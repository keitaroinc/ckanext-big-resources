# ckanext-big-resources

Ckan extension that overwrites the upload and download of the resources. 
the extension breaks the resources into chunks and streams the response. This extension is usefull if We want to configure the chunk size of upload and download in order to use of the server resources in more efficient way.


## Requirements


Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | Yes           |


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-big-resources:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/blagojabozinovski/ckanext-big-resources.git
    cd ckanext-big-resources
    pip install -e .
	pip install -r requirements.txt

3. Add `big-resources` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** The chunk size for upload and download can be set up in production.ini as shown below


	ckanext.big_resources.chunk_upload = number_in_bytes
    ckanext.big_resources.chunk_upload = number_in_bytes

The default value is 2048



## Developer installation

To install ckanext-big-resources for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/blagojabozinovski/ckanext-big-resources.git
    cd ckanext-big-resources
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-big-resources

If ckanext-big-resources should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
