# Github pages for python-oca
To update the 'gh-pages' re-create the docs in the 'master' branch and commit the generated html pages on 'gh-pages'.

```
git checkout master
cd docs
PYTHONPATH=.. make html
cd ..
git checkout gh-pages
cp -a docs/_build/html/* .
rm -r oca docs
git status
```
