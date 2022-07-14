import shutil
import urllib.parse
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

ARTIFACTS_URL = 'https://sonic-build.azurewebsites.net/api/sonic/artifacts'
BRANCH_NAME = '202205'
BUILD_ID = '118833'

DOCKER_IMAGES = [
    'docker-dhcp-relay',
    'docker-fpm-frr',
    'docker-teamd',
    'docker-syncd-vs',
    'docker-router-advertiser',
    'docker-orchagent',
    'docker-database',
    'docker-lldp',
    'docker-gbsyncd-vs',
]


def download_directory(directory: str):
    params = urllib.parse.urlencode({
        'branchName': BRANCH_NAME,
        'buildId': BUILD_ID,
        'format': 'zip',
        'platform': 'vs',
        'target': directory,
    })
    path = Path(directory)
    path.parent.mkdir(parents=True, exist_ok=True)
    url = f'{ARTIFACTS_URL}?{params}'
    print(f"Download {url}")
    with urllib.request.urlopen(url) as src:
        with zipfile.ZipFile(BytesIO(src.read())) as zip:
            # zip files already contain the parent directory sonic-buildimage.vs
            zip.extractall()


def download_image(image: str) -> None:
    file = f'sonic-buildimage.vs/target/{image}.gz'
    params = urllib.parse.urlencode({
        'branchName': BRANCH_NAME,
        'buildId': BUILD_ID,
        'platform': 'vs',
        'target': f'target/{image}.gz',
    })
    path = Path(file)
    url = f'{ARTIFACTS_URL}?{params}'
    print(f"Download {url}")
    with urllib.request.urlopen(url) as src:
        with path.open(mode='wb') as dest:
            shutil.copyfileobj(src, dest)


download_directory('target/debs/bullseye')
download_directory('target/files/bullseye')
download_directory('target/python-wheels/bullseye')

for image in DOCKER_IMAGES:
    download_image(image)

# def get_all_bins(target_path: str, extension: str) -> None:
#     print(f'Fetching {target_path}*{extension}')
#     os.makedirs(target_path, exist_ok=True)
#
#     req = urllib.request.urlopen(UPSTREAM_PREFIX + target_path)
#     data = req.read().decode()
#
#     class Downloader(HTMLParser):
#         artifact = None
#
#         def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
#             if tag == 'a':
#                 pprint.pprint(attrs)
#                 for attr, val in attrs:
#                     if attr == 'href' and val.endswith(extension):
#                         self.artifact = {'href': val}
#
#         def handle_data(self, data: str) -> None:
#             if self.artifact:
#                 self.artifact['target'] = data
#
#         def handle_endtag(self, tag: str) -> None:
#             if self.artifact and tag == 'a':
#                 self.download_file(target=self.artifact['target'], url=self.artifact['href'])
#                 self.artifact = None
#
#         @staticmethod
#         def download_file(target: str, url: str) -> None:
#             path = Path(target)
#             path.parent.mkdir(parents=True, exist_ok=True)
#             src = urllib.request.urlopen(UPSTREAM_PREFIX + url)
#             print(f'{target} from {url}')
#             with path.open(mode='wb') as dest:
#                 shutil.copyfileobj(src, dest)
#
#     parser = Downloader()
#     parser.feed(data)
#     print()
#
#
# get_all_bins('target/debs/stretch/', '.deb')
# get_all_bins('target/files/stretch/', '.ko')
# get_all_bins('target/python-debs/', '.deb')
# get_all_bins('target/python-wheels/', '.whl')
# get_all_bins('target/', '.gz')
