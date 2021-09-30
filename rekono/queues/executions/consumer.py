import rq
from django_rq import job
from executions.models import Execution
from processes.executor import success_callback
from queues.executions import producer
from queues.executions import utils as queue_utils
from queues.executions.constants import finding_relations
from rq.job import Job
from tools import utils as tool_utils
from tools.enums import FindingType
from tools.models import Configuration, Input, Intensity, Tool


@job('executions-queue')
def execute(
    execution: Execution,
    tool: Tool,
    configuration: Configuration,
    intensity: Intensity,
    inputs: list,
    parameters: list,
    previous_findings: list
) -> None:
    current_job = rq.get_current_job()
    execution.rq_job_id = current_job.id
    execution.save()
    if not previous_findings:
        if current_job._dependency_ids:
            previous_findings = process_dependencies(
                execution,
                intensity,
                inputs,
                parameters,
                current_job
            )
    tool_class = tool_utils.get_tool_class_by_name(tool.name)
    tool = tool_class(
        execution=execution,
        tool=tool,
        configuration=configuration,
        inputs=inputs,
        intensity=intensity
    )
    tool.run(parameters=parameters, previous_findings=previous_findings)
    return tool


def process_dependencies(
    execution: Execution,
    intensity: Intensity,
    inputs: list,
    parameters: list,
    current_job: Job
) -> list:
    findings = queue_utils.get_findings_from_dependencies(current_job._dependency_ids)
    if not findings:
        return []
    new_jobs_ids = []
    jobs = get_new_jobs_from_findings(findings, inputs)
    for job_counter in jobs.keys():
        if job_counter == 0:
            continue
        execution = Execution.objects.create(request=execution.request, step=execution.step)
        job = producer.execute(
            execution,
            intensity,
            inputs,
            parameters=parameters,
            previous_findings=jobs[job_counter],
            callback=success_callback,
            at_front=True
        )
        new_jobs_ids.append(job.id)
    queue_utils.update_new_dependencies(current_job.id, new_jobs_ids, parameters)
    return jobs[0]


def get_new_jobs_from_findings(findings: dict, inputs: list) -> dict:
    job_counter = 0
    jobs = {
        job_counter: []
    }
    for input_type in finding_relations.keys():
        input_class = tool_utils.get_finding_class_by_type(input_type)
        filter = [i for i in inputs if (
            i.type == input_type or
            (
                i.type == FindingType.URL and
                input_type in [FindingType.HOST, FindingType.ENUMERATION]
            ))]
        if not filter or input_type not in findings:
            continue
        for i in filter:
            if finding_relations[input_type]:
                relations_found = False
                for finding in findings[input_type]:
                    for relation in finding_relations[input_type]:
                        if hasattr(finding, relation.name.lower()):
                            attribute = getattr(finding, relation.name.lower(), None)
                            if attribute:
                                relations_found = True
                                for jc in jobs.copy():
                                    if attribute in jobs[jc]:
                                        if i.selection == Input.InputSelection.ALL:
                                            jobs[jc].append(finding)
                                        else:
                                            related_items = [
                                                f for f in jobs[jc]
                                                if not isinstance(f, input_class)
                                            ]
                                            if len(related_items) < len(jobs[jc]):
                                                jobs[job_counter] = related_items.copy()
                                                jobs[job_counter].append(finding)
                                                job_counter += 1
                                            else:
                                                jobs[jc].append(finding)
                                break
                    if not relations_found:
                        for jc in jobs.copy():
                            jobs[jc].append(finding)
            else:
                if i.selection == Input.InputSelection.ALL:
                    for jc in jobs.copy():
                        jobs[jc].extend(findings[input_type])
                else:
                    aux = jobs[job_counter].copy()
                    for finding in findings[input_type]:
                        jobs[job_counter] = aux.copy()
                        jobs[job_counter].append(finding)
                        job_counter += 1
    return jobs