#/bin/bash


rm -rf noresqa

# Check if git-lfs is installed
if git lfs --version >/dev/null 2>&1; then
  echo "Git LFS is installed."
else
  echo "Git LFS is not installed. Please install git-lfs first."
  echo "You may check tools/install_gitlfs.md for guidelines"
  exit 1
fi

GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/shimhz/noresqa_versa.git
cd Noresqa
pip install -e .
cd ..
