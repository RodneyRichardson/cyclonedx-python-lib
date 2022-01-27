# encoding: utf-8

# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.
import base64
from datetime import datetime, timezone
from decimal import Decimal
from typing import List

from packageurl import PackageURL

from cyclonedx.model import Encoding, ExternalReference, ExternalReferenceType, HashType, LicenseChoice, Note, \
    NoteText, OrganizationalContact, OrganizationalEntity, Property, Tool, XsUri, DataClassification, DataFlow
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.issue import IssueClassification, IssueType
from cyclonedx.model.release_note import ReleaseNotes
from cyclonedx.model.service import Service
from cyclonedx.model.vulnerability import ImpactAnalysisState, ImpactAnalysisJustification, ImpactAnalysisResponse, \
    ImpactAnalysisAffectedStatus, Vulnerability, VulnerabilityCredits, VulnerabilityRating, VulnerabilitySeverity, \
    VulnerabilitySource, VulnerabilityScoreSource, VulnerabilityAdvisory, VulnerabilityReference, \
    VulnerabilityAnalysis, BomTarget, BomTargetVersionRange

MOCK_TIMESTAMP: datetime = datetime(2021, 12, 31, 10, 0, 0, 0).replace(tzinfo=timezone.utc)
MOCK_UUID_1 = 'be2c6502-7e9a-47db-9a66-e34f729810a3'
MOCK_UUID_2 = '17e3b199-dc0b-42ef-bfdd-1fa81a1e3eda'
MOCK_UUID_3 = '0b049d09-64c0-4490-a0f5-c84d9aacf857'
MOCK_UUID_4 = 'cd3e9c95-9d41-49e7-9924-8cf0465ae789'
MOCK_UUID_5 = 'bb5911d6-1a1d-41c9-b6e0-46e848d16655'
MOCK_UUID_6 = 'df70b5f1-8f53-47a4-be48-669ae78795e6'


def get_bom_with_component_setuptools_basic() -> Bom:
    bom = Bom(
        components=[Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ), license_str='MIT License', author='Test Author'
        )]
    )
    return bom


def get_bom_with_component_setuptools_with_cpe() -> Bom:
    bom = Bom(
        components=[Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ), license_str='MIT License', author='Test Author',
            cpe='cpe:2.3:a:python:setuptools:50.3.2:*:*:*:*:*:*:*'
        )]
    )
    return bom


def get_bom_with_component_setuptools_no_component_version() -> Bom:
    bom = Bom(
        components=[Component(
            name='setuptools', bom_ref='pkg:pypi/setuptools?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', qualifiers='extension=tar.gz'
            ), license_str='MIT License', author='Test Author'
        )]
    )
    return bom


def get_bom_with_component_setuptools_with_release_notes() -> Bom:
    bom = Bom(
        components=[Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ), license_str='MIT License', author='Test Author',
            release_notes=get_release_notes()
        )]
    )
    return bom


def get_bom_with_component_setuptools_with_vulnerability() -> Bom:
    bom = Bom()
    component = Component(
        name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
        purl=PackageURL(
            type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
        ), license_str='MIT License', author='Test Author'
    )
    vulnerability = Vulnerability(
        bom_ref='my-vuln-ref-1', id='CVE-2018-7489', source=get_vulnerability_source_nvd(),
        references=[
            VulnerabilityReference(id='SOME-OTHER-ID', source=VulnerabilitySource(
                name='OSS Index', url=XsUri('https://ossindex.sonatype.org/component/pkg:pypi/setuptools')
            ))
        ],
        ratings=[
            VulnerabilityRating(
                source=get_vulnerability_source_nvd(), score=Decimal(9.8), severity=VulnerabilitySeverity.CRITICAL,
                method=VulnerabilityScoreSource.CVSS_V3,
                vector='AN/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', justification='Some justification'
            ),
            VulnerabilityRating(
                source=get_vulnerability_source_owasp(), score=Decimal(2.7), severity=VulnerabilitySeverity.LOW,
                method=VulnerabilityScoreSource.CVSS_V3,
                vector='AV:L/AC:H/PR:N/UI:R/S:C/C:L/I:N/A:N', justification='Some other justification'
            )
        ],
        cwes=[22, 33], description='A description here', detail='Some detail here',
        recommendation='Upgrade',
        advisories=[
            VulnerabilityAdvisory(url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2018-7489')),
            VulnerabilityAdvisory(url=XsUri('http://www.securitytracker.com/id/1040693'))
        ],
        created=datetime(year=2021, month=9, day=1, hour=10, minute=50, second=42, microsecond=51979,
                         tzinfo=timezone.utc),
        published=datetime(year=2021, month=9, day=2, hour=10, minute=50, second=42, microsecond=51979,
                           tzinfo=timezone.utc),
        updated=datetime(year=2021, month=9, day=3, hour=10, minute=50, second=42, microsecond=51979,
                         tzinfo=timezone.utc),
        credits=VulnerabilityCredits(
            organizations=[
                get_org_entity_1()
            ],
            individuals=[
                OrganizationalContact(name='A N Other', email='someone@somewhere.tld', phone='+44 (0)1234 567890'),
            ]
        ),
        tools=[
            Tool(vendor='CycloneDX', name='cyclonedx-python-lib')
        ],
        analysis=VulnerabilityAnalysis(
            state=ImpactAnalysisState.EXPLOITABLE, justification=ImpactAnalysisJustification.REQUIRES_ENVIRONMENT,
            responses=[ImpactAnalysisResponse.CAN_NOT_FIX], detail='Some extra detail'
        ),
        affects_targets=[
            BomTarget(
                ref=component.purl.to_string() if component.purl else component.to_package_url().to_string(),
                versions=[BomTargetVersionRange(
                    version_range='49.0.0 - 54.0.0', status=ImpactAnalysisAffectedStatus.AFFECTED
                )]
            )
        ]
    )
    component.add_vulnerability(vulnerability=vulnerability)
    bom.add_component(component=component)
    return bom


def get_bom_with_component_toml_1() -> Bom:
    bom = Bom(components=[
        Component(
            name='toml', version='0.10.2', bom_ref='pkg:pypi/toml@0.10.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='toml', version='0.10.2', qualifiers='extension=tar.gz'
            ), hashes=[
                HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
            ], external_references=[
                get_external_reference_1()
            ]
        )
    ])
    return bom


def get_bom_just_complete_metadata() -> Bom:
    bom = Bom()
    bom.metadata.component = Component(
        name='cyclonedx-python-lib', version='1.0.0', component_type=ComponentType.LIBRARY
    )
    return bom


def get_bom_with_services_simple() -> Bom:
    bom = Bom(services=[
        Service(name='my-first-service'),
        Service(name='my-second-service')
    ])
    bom.metadata.component = Component(
        name='cyclonedx-python-lib', version='1.0.0', component_type=ComponentType.LIBRARY
    )
    return bom


def get_bom_with_services_complex() -> Bom:
    bom = Bom(services=[
        Service(
            name='my-first-service', bom_ref='my-specific-bom-ref-for-my-first-service',
            provider=get_org_entity_1(), group='a-group', version='1.2.3',
            description='Description goes here', endpoints=[
                XsUri('/api/thing/1'),
                XsUri('/api/thing/2')
            ],
            authenticated=False, x_trust_boundary=True, data=[
                DataClassification(flow=DataFlow.OUTBOUND, classification='public')
            ],
            licenses=[
                LicenseChoice(license_expression='Commercial')
            ],
            external_references=[
                get_external_reference_1()
            ],
            properties=get_properties_1(),
            release_notes=get_release_notes()
        ),
        Service(name='my-second-service')
    ])
    bom.metadata.component = Component(
        name='cyclonedx-python-lib', version='1.0.0', component_type=ComponentType.LIBRARY
    )
    return bom


def get_external_reference_1() -> ExternalReference:
    return ExternalReference(
        reference_type=ExternalReferenceType.DISTRIBUTION,
        url='https://cyclonedx.org',
        comment='No comment',
        hashes=[
            HashType.from_composite_str(
                'sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        ]
    )


def get_org_entity_1() -> OrganizationalEntity:
    return OrganizationalEntity(
        name='CycloneDX', urls=[XsUri('https://cyclonedx.org')], contacts=[
            OrganizationalContact(name='Paul Horton', email='paul.horton@owasp.org'),
            OrganizationalContact(name='A N Other', email='someone@somewhere.tld',
                                  phone='+44 (0)1234 567890')
        ]
    )


def get_properties_1() -> List[Property]:
    return [
        Property(name='key1', value='val1'),
        Property(name='key2', value='val2')
    ]


def get_release_notes() -> ReleaseNotes:
    text_content: str = base64.b64encode(
        bytes('Some simple plain text', encoding='UTF-8')
    ).decode(encoding='UTF-8')

    return ReleaseNotes(
        type='major', title="Release Notes Title",
        featured_image=XsUri('https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'),
        social_image=XsUri('https://cyclonedx.org/cyclonedx-icon.png'),
        description="This release is a test release", timestamp=MOCK_TIMESTAMP,
        aliases=[
            "First Test Release"
        ],
        tags=['test', 'alpha'],
        resolves=[
            IssueType(
                classification=IssueClassification.SECURITY, id='CVE-2021-44228', name='Apache Log3Shell',
                description='Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features...',
                source_name='NVD', source_url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228'),
                references=[
                    XsUri('https://logging.apache.org/log4j/2.x/security.html'),
                    XsUri('https://central.sonatype.org/news/20211213_log4shell_help')
                ]
            )
        ],
        notes=[
            Note(
                text=NoteText(
                    content=text_content, content_type='text/plain; charset=UTF-8',
                    content_encoding=Encoding.BASE_64
                ), locale='en-GB'
            ),
            Note(
                text=NoteText(
                    content=text_content, content_type='text/plain; charset=UTF-8',
                    content_encoding=Encoding.BASE_64
                ), locale='en-US'
            )
        ],
        properties=get_properties_1()
    )


def get_vulnerability_source_nvd() -> VulnerabilitySource:
    return VulnerabilitySource(name='NVD', url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2018-7489'))


def get_vulnerability_source_owasp() -> VulnerabilitySource:
    return VulnerabilitySource(name='OWASP', url=XsUri('https://owasp.org'))