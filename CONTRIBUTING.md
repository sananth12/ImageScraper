# Contributing to ImageScraper

## Code style:
* Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) standards.
* Name variables with underscores and lowercase letters. Not camelCase.


## Git commit messages:
* Limit the first line to 72 characters or less
* Reference issues and pull requests
* Consider starting the commit message with an applicable emoji:
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :scroll: `:scroll:` when writing docs
    * :penguin: `:penguin:` when fixing something on Linux
    * :apple: `:apple:` when fixing something on Mac OS
    * :checkered_flag: `:checkered_flag:` when fixing something on Windows
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :wrench: `:wrench:` when doing CI


## Making changes:
* Make your changes in a new git branch:

    ```sh
    git checkout -b fix-branch master
    ```

* Create your patch, *including appropriate test cases*.
* Commit your changes using a descriptive commit message as mentioned above

    ```sh
    git commit -a
    ```

* Build your changes locally to ensure all the tests pass:

    ```sh
    nosetests
    ```

* Push your branch to GitHub:

    ```sh
    git push origin my-fix-branch
    ```

* In GitHub, send a pull request to `ImageScraper:master`.

Thank you for your contribution!
