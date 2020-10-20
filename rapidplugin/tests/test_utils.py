# Copyright 2020 Software Improvement Group
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

import os
import pytest
from utils.utils import MavenUtils
from pathlib import Path

DOWNLOAD_URL_DATA = [
    ("https://repo1.maven.org/maven2/ai/api/libai/1.6.12/libai-1.6.12-sources.jar")
]

@pytest.fixture(scope='session')
def sources_dir(tmp_path_factory):
    yield tmp_path_factory.mktemp("sources")

@pytest.mark.parametrize('url', DOWNLOAD_URL_DATA)
def test_download_jar(url, sources_dir):
    source_path = MavenUtils.download_jar(url, sources_dir)
    assert str(source_path) == os.path.join(sources_dir, 'tmp')


def test_tailor_input(in_payload, out_payload):
    assert True

