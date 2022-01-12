<template>
  <div>
    <TableHeader :filters="filters" add="process-modal" @filter="fetchData"/>
    <b-table striped borderless head-variant="dark" :fields="processesFields" :items="processes">
      <template #cell(tags)="row">
        <b-form-tags no-outer-focus :value="row.item.tags" placeholder="" remove-on-delete size="md" tag-variant="dark" @input="updateProcess(row.item, $event)"/>
      </template>
      <template #cell(likes)="row">
        {{ row.item.likes }}
        <b-button variant="outline">
          <b-icon variant="danger" v-if="row.item.liked" icon="heart-fill" @click="dislike('processes', row.item.id); fetchData()"/>
          <b-icon variant="danger" v-if="!row.item.liked" icon="heart" @click="like('processes', row.item.id); fetchData()"/>
        </b-button>
      </template>
      <template #cell(actions)="row">
        <b-button @click="row.toggleDetails" variant="outline" class="mr-2" v-b-tooltip.hover title="Details">
          <b-icon v-if="!row.detailsShowing" variant="dark" icon="eye-fill"/>
          <b-icon v-if="row.detailsShowing" variant="secondary" icon="eye-slash-fill"/>
        </b-button>
        <b-button variant="outline" class="mr-2" :disabled="row.item.steps.length === 0" v-b-tooltip.hover title="Execute" @click="showExecuteForm(row.item)" v-b-modal.execute-modal>
          <b-icon variant="success" icon="play-circle-fill"/>
        </b-button>
        <b-dropdown variant="outline" right>
          <template #button-content>
            <b-icon variant="dark" icon="three-dots-vertical"/>
          </template>
          <b-dropdown-item @click="showStepForm(row.item)" v-b-modal.step-modal :disabled="$store.state.role !== 'Admin' && $store.state.user !== row.item.creator.id">
            <b-icon variant="success" icon="plus-square"/>
            <label class="ml-1" variant="dark">Add Step</label>
          </b-dropdown-item>
          <b-dropdown-item variant="dark" @click="showProcessForm(row.item)" v-b-modal.process-modal :disabled="$store.state.role !== 'Admin' && $store.state.user !== row.item.creator.id">
            <b-icon icon="pencil-square"/>
            <label class="ml-1">Edit</label>
          </b-dropdown-item>
          <b-dropdown-item variant="danger" @click="selectProcess(row.item)" v-b-modal.delete-process-modal :disabled="$store.state.role !== 'Admin' && $store.state.user !== row.item.creator.id">
            <b-icon icon="trash-fill"/>
            <label class="ml-1">Delete</label>
          </b-dropdown-item>
        </b-dropdown>
      </template>
      <template #row-details="row">
        <b-card>
          <p>{{ row.item.description }}</p>
          <b-table striped borderless small head-variant="light" :fields="stepsFields" :items="row.item.steps">
            <template #cell(icon)="step">
              <b-link :href="step.item.tool.reference" target="_blank">
                <b-img :src="step.item.tool.icon" width="100" height="50"/>
              </b-link>
            </template>
            <template #cell(actions)="step">
              <b-dropdown variant="outline" right>
                <template #button-content>
                  <b-icon variant="secondary" icon="three-dots-vertical"/>
                </template>
                <b-dropdown-item variant="dark" @click="showStepForm(row.item, step.item)" v-b-modal.step-modal :disabled="$store.state.role !== 'Admin' && $store.state.user !== row.item.creator.id">
                  <b-icon icon="pencil-square"/>
                  <label class="ml-1">Edit</label>
                </b-dropdown-item>
                <b-dropdown-item variant="danger" @click="selectStep(row.item, step.item)" v-b-modal.delete-step-modal :disabled="$store.state.role !== 'Admin' && $store.state.user !== row.item.creator.id">
                  <b-icon icon="trash-fill"/>
                  <label class="ml-1">Delete</label>
                </b-dropdown-item>
              </b-dropdown>
            </template>
          </b-table>
        </b-card>
      </template>
    </b-table>
    <Pagination :page="page" :limit="limit" :limits="limits" :total="total" name="processes" @pagination="pagination"/>
    <Deletion id="delete-process-modal"
      title="Delete Process"
      @deletion="deleteProcess"
      @clean="cleanSelection"
      v-if="selectedProcess !== null">
      <span><strong>{{ selectedProcess.name }}</strong> process</span>
    </Deletion>
    <Deletion id="delete-step-modal"
      title="Delete Step"
      @deletion="deleteStep"
      @clean="cleanSelection"
      v-if="selectedProcess !== null && selectedStep !== null">
      <span><strong>{{ this.selectedStep.tool.name }}</strong> step from <strong>{{ selectedProcess.name }}</strong> process</span>
    </Deletion>
    <ProcessForm id="process-modal" :process="selectedProcess" :initialized="processForm" @confirm="confirm" @clean="cleanSelection"/>
    <StepForm id="step-modal" :process="selectedProcess" :step="selectedStep" :initialized="stepForm" @confirm="confirm" @clean="cleanSelection"/>
    <TaskForm id="execute-modal" :process="selectedProcess" :initialized="taskForm" @confirm="confirm" @clean="cleanSelection"/>
  </div>
</template>

<script>
import Processes from '@/backend/processes'
import { stages } from '@/backend/constants'
import Deletion from '@/common/Deletion.vue'
import TableHeader from '@/common/TableHeader.vue'
import Pagination from '@/common/Pagination.vue'
import AlertMixin from '@/common/mixin/AlertMixin.vue'
import PaginationMixin from '@/common/mixin/PaginationMixin.vue'
import LikeMixin from '@/common/mixin/LikeMixin.vue'
import ProcessForm from '@/modals/ProcessForm.vue'
import StepForm from '@/modals/StepForm.vue'
import TaskForm from '@/modals/TaskForm.vue'
const ProcessApi = Processes.ProcessApi
const StepApi = Processes.StepApi
export default {
  name: 'processesPage',
  mixins: [AlertMixin, PaginationMixin, LikeMixin],
  data () {
    return {
      processes: this.fetchData(),
      processesFields: [
        { key: 'name', label: 'Process', sortable: true },
        { key: 'tags', sortable: true },
        { key: 'steps.length', label: 'Steps', sortable: true },
        { key: 'creator.username', label: 'Creator', sortable: true },
        { key: 'likes', sortable: true },
        { key: 'actions', sortable: false }
      ],
      stepsFields: [
        { key: 'icon', sortable: false },
        { key: 'tool.name', label: 'Tool', sortable: true },
        { key: 'configuration.name', label: 'Configuration', sortable: true },
        { key: 'tool.stage_name', label: 'Stage', sortable: true },
        { key: 'priority', sortable: true },
        { key: 'actions', sortable: false }
      ],
      taskForm: false,
      processForm: false,
      stepForm: false,
      selectedProcess: null,
      selectedStep: null,
      filters: []
    }
  },
  components: {
    Deletion,
    TableHeader,
    Pagination,
    ProcessForm,
    StepForm,
    TaskForm
  },
  watch: {
    processes () {
      this.filters = [
        { name: 'Tags', filterField: 'tags__name__in', type: 'tags' },
        { name: 'Stage', values: stages, valueField: 'id', textField: 'value', filterField: 'steps__tool__stage' },
        { name: 'Creator', filterField: 'creator__username__icontains', type: 'text' },
        { name: 'Favourities', values: [{ value: true, text: 'True' }, { value: false, text: 'False' }], valueField: 'value', textField: 'text', filterField: 'liked' }
      ]
    }
  },
  methods: {
    fetchData (filter = null) {
      ProcessApi.getPaginatedProcesses(this.getPage(), this.getLimit(), filter).then(data => {
        this.total = data.count
        this.processes = data.results
      })
    },
    updateProcess (process, tags) {
      ProcessApi.updateProcess(process.id, process.name, process.description, tags)
    },
    deleteProcess () {
      ProcessApi.deleteProcess(this.selectedProcess.id)
        .then(() => {
          this.$bvModal.hide('delete-process-modal')
          this.warning(this.selectedProcess.name, 'Process deleted successfully')
          this.fetchData()
        })
        .catch(() => {
          this.danger(this.selectedProcess.name, 'Unexpected error in process deletion')
        })
    },
    deleteStep () {
      StepApi.deleteStep(this.selectedStep.id)
        .then(() => {
          this.$bvModal.hide('delete-step-modal')
          this.warning(`${this.processName} - ${this.selectedStep.name}`, 'Step deleted successfully')
          this.fetchData()
        })
        .catch(() => {
          this.danger(this.processName, 'Unexpected error in step deletion')
        })
    },
    showExecuteForm (process, step = null) {
      this.taskForm = true
      if (step !== null) {
        this.selectStep(process, step)
      } else {
        this.selectProcess(process)
      }
    },
    showProcessForm (process, step = null) {
      this.processForm = true
      if (step !== null) {
        this.selectStep(process, step)
      } else {
        this.selectProcess(process)
      }
    },
    showStepForm (process, step = null) {
      this.stepForm = true
      if (step !== null) {
        this.selectStep(process, step)
      } else {
        this.selectProcess(process)
      }
    },
    selectProcess (process) {
      this.selectedProcess = process
    },
    selectStep (process, step) {
      this.selectProcess(process)
      this.selectedStep = step
    },
    cleanSelection () {
      this.taskForm = false
      this.processForm = false
      this.stepForm = false
      this.selectedProcess = null
      this.selectedStep = null
    }
  }
}
</script>