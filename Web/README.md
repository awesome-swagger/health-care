# StartStudio Angular 2 Template v1.0.0
[**SEE WIKI PAGES**](https://dev.izeni.net/izeni/startstudio-angular-template/wikis/home) in this repo for more detailed introductions to the various features of this template.

This project was initially generated with [angular-cli](https://github.com/angular/angular-cli) version 1.0.0-beta.19-3.

## Setup

#### Quick
```bash
bash <(wget -qO- https://dev.izeni.net/izeni/startstudio-angular-template/raw/develop/startproject.sh) <project_name>
yarn global add angular-cli
yarn install
```

#### Manual
Set your project name as an environment variable
```bash
care-adopt-frontend=[your project name here]
```
And run the following commands:
```bash
git clone -b cli --single-branch git@dev.izeni.net:izeni/startstudio-angular-template.git
mv startstudio-angular-template $care-adopt-frontend
cd $care-adopt-frontend
find . -type f -print0 | xargs -0 sed -i "s/care-adopt-frontend/$care-adopt-frontend/g"
yarn global add angular-cli
yarn install
```

#### Set git url
Don't forget to change the git origin to match your project's, which will differ slightly depending on the method you used to clone:  
Quick:
```bash
git init
git remote add origin <remote-url-of-project>
```
Manual:
```bash
git remote set-url origin <remote-url-of-project>
```

## Development server
Run `yarn start` (which runs `ng serve` on port 9000) for a dev server. Navigate to `http://localhost:9000/`. The app will automatically reload if you change any of the source files.

## API config
To change your backend api url, change the `apiHost` property of the appropriate module in `src/environments`.

## Code scaffolding
Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive/pipe/service/class`. You can also give a path, relative to `src/app` for the `component-name` and the files will be placed in that location, and (usually) added correctly to the nearest module.

## Build
Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build or `-staging` for a staging build.

## Running unit tests
Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests
Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Before running the tests make sure you are serving the app via `ng serve`.

## Further help
To get more help on the `angular-cli` use `ng --help` or go check out the [Angular-CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
