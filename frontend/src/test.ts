// This file is required by karma.conf.js and loads recursively all the .spec and framework files

import { getTestBed } from '@angular/core/testing';
import { platformBrowser } from '@angular/platform-browser';
import { BrowserTestingModule } from '@angular/platform-browser/testing';

// First, initialize the Angular testing environment.
getTestBed().initTestEnvironment(
  BrowserTestingModule,
  platformBrowser(), {
    teardown: { destroyAfterEach: false }
}
);
