from findings.enums import Severity
from findings.models import Endpoint, Exploit, Technology, Vulnerability
from testing.tools.base import ToolParserTest


class JoomScanParserTest(ToolParserTest):
    '''Test cases for JoomScan parser.'''

    tool_name = 'JoomScan'

    def test_report_with_exploits(self) -> None:
        '''Test to parse report with CVEs and exploits.'''
        expected = [
            {
                'model': Technology,
                'name': 'Joomla',
                'version': '3.4.5',
                'description': 'Joomla 3.4.5',
                'reference': 'https://www.joomla.org/'
            },
            {
                'model': Vulnerability,
                'name': '3.4.4 < 3.6.4 - Account Creation / Privilege Escalation',
                'cve': 'CVE-2016-8870'
            },
            {
                'model': Vulnerability,
                'name': '3.4.4 < 3.6.4 - Account Creation / Privilege Escalation',
                'cve': 'CVE-2016-8869'
            },
            {
                'model': Exploit,
                'title': '3.4.4 < 3.6.4 - Account Creation / Privilege Escalation',
                'edb_id': 40637,
                'reference': 'https://www.exploit-db.com/exploits/40637/'
            },
            {'model': Vulnerability, 'name': 'Core Remote Privilege Escalation Vulnerability', 'cve': 'CVE-2016-9838'},
            {
                'model': Exploit,
                'title': 'Core Remote Privilege Escalation Vulnerability',
                'edb_id': 41157,
                'reference': 'https://www.exploit-db.com/exploits/41157/'
            },
            {'model': Vulnerability, 'name': 'Directory Traversal Vulnerability', 'cve': 'CVE-2015-8565'},
            {'model': Vulnerability, 'name': 'Directory Traversal Vulnerability', 'cve': 'CVE-2015-8564'},
            {'model': Vulnerability, 'name': 'Core Cross Site Request Forgery Vulnerability', 'cve': 'CVE-2015-8563'},
            {'model': Vulnerability, 'name': 'Core Security Bypass Vulnerability', 'cve': 'CVE-2016-9081'},
            {'model': Vulnerability, 'name': 'Core Arbitrary File Upload Vulnerability', 'cve': 'CVE-2016-9836'},
            {'model': Vulnerability, 'name': 'Information Disclosure Vulnerability', 'cve': 'CVE-2016-9837'},
            {'model': Vulnerability, 'name': 'PHPMailer Remote Code Execution Vulnerability', 'cve': 'CVE-2016-10033'},
            {
                'model': Exploit,
                'title': 'PHPMailer Remote Code Execution Vulnerability',
                'edb_id': 40969,
                'reference': 'https://www.exploit-db.com/exploits/40969/'
            },
            {
                'model': Vulnerability,
                'name': 'PPHPMailer Incomplete Fix Remote Code Execution Vulnerability',
                'cve': 'CVE-2016-10045'
            },
            {
                'model': Exploit,
                'title': 'PPHPMailer Incomplete Fix Remote Code Execution Vulnerability',
                'edb_id': 40969,
                'reference': 'https://www.exploit-db.com/exploits/40969/'
            },
            {'model': Endpoint, 'endpoint': '/administrator/'}
        ]
        super().check_tool_output_parser('exploitable.txt', expected)

    def test_report_without_cves_and_exploits(self) -> None:
        '''Test to parse report without CVEs and exploits.'''
        expected = [
            {
                'model': Technology,
                'name': 'Joomla',
                'version': '3.7.0',
                'description': 'Joomla 3.7.0',
                'reference': 'https://www.joomla.org/'
            },
            {'model': Endpoint, 'endpoint': '/administrator/'},
            {'model': Endpoint, 'endpoint': '/backup/config.php.bak'},
            {'model': Endpoint, 'endpoint': '/config.php'},
            {'model': Endpoint, 'endpoint': '/error.php'},
            {'model': Endpoint, 'endpoint': '/static'},
            {
                'model': Vulnerability,
                'name': 'Backup files found',
                'severity': Severity.HIGH,
                'cwe': 'CWE-530'
            },
            {
                'model': Vulnerability,
                'name': 'Configuration files found',
                'severity': Severity.MEDIUM,
                'cwe': 'CWE-497'
            },
            {
                'model': Vulnerability,
                'name': 'Full path disclosure',
                'severity': Severity.LOW,
                'cwe': 'CWE-497'
            },
            {
                'model': Vulnerability,
                'name': 'Directory listing',
                'severity': Severity.LOW,
                'cwe': 'CWE-548'
            }
        ]
        super().check_tool_output_parser('not-exploitable.txt', expected)

    def test_report_not_joomla(self) -> None:
        '''Test to parse report from not Joomla service.'''
        super().check_tool_output_parser('not-joomla.txt', [])