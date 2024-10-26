# Contributing to sm-2

Welcome to sm-2!

In this short guide, you will get a quick overview of how you can contribute to the sm-2 project.

## Reporting issues

If you encounter an issue with sm-2 and would like to report it, you'll first want to make sure you're using the latest version of sm-2.

The latest version of sm-2 can be found under [releases](https://github.com/joshdavham/sm-2/releases) and you can verify the version of your current installation with the following command:
```
pip show sm-2
```

Once you've confirmed your version, please report your issue in the [issues tab](https://github.com/joshdavham/sm-2/issues).

## Contributing code

### Local setup

**Step 1**: Start by forking this repo, then cloning it to your local machine.

**Step 2**: Create a new local branch where you will implement your changes.

### Develop

Install the `sm-2` python package locally in editable mode from the src with
```
pip install -e .
```

Now you're ready to make changes to `src/sm_2` and see your changes reflected immediately!

### Test

sm-2 uses [pytest](https://docs.pytest.org) to run its tests. In order for your contribution to be accepted, your code must pass the tests.

You can install `pytest` with
```
pip install pytest
```

Run the tests with:
```
pytest
```

Additionally, you're encouraged to contribute your own tests to [tests/test_sm_2.py](tests/test_sm_2.py) to help make sm-2 more reliable!

### Submit a pull request

To submit a pull request, commit your local changes to your branch then push the branch to your fork. You can now open a pull request.