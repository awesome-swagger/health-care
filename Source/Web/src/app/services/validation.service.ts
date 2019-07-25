import { Injectable } from '@angular/core';

// @inspired by: https://coryrylan.com/blog/angular-2-form-builder-and-validation-management
// form validation examples: http://blog.thoughtram.io/angular/2016/03/14/custom-validators-in-angular-2.html
@Injectable()
export class ValidationService {

  constructor() { }

  public getValidatorErrorMessage(validatorName: string) {
    let config = {
      required: 'Required',
      invalidEmailAddress: 'Invalid email address',
      invalidPassword: 'Invalid password. Password must be at least 6 characters long, and contain a number.',
    };
    return config[validatorName];
  }

  public emailValidator(control: { value: string }) {
    // RFC 2822 compliant regex for email validation
    if (control.value.match(/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/)) {
      return null;
    } else {
      return { 'invalidEmailAddress': true };
    }
  }

  public passwordValidator(control: { value: string }) {
    // {6,100}           - Assert password is between 6 and 100 characters
    // (?=.*[0-9])       - Assert a string has at least one number
    if (control.value.match(/^(?=.*[0-9])[a-zA-Z0-9!@#$%^&*]{6,100}$/)) {
      return null;
    } else {
      return { 'invalidPassword': true };
    }
  }

  public phoneInternationalValidator(control: { value: string }) {
    // {6,100}           - Assert password is between 6 and 100 characters
    // (?=.*[0-9])       - Assert a string has at least one number
    // tslint:disable-next-line:max-line-length
    let regex = /(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]‌)\s*)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)([2-9]1[02-9]‌|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})/;
    if (control.value.match(regex)) {
      return null;
    } else {
      return { 'invalidInternationalPhoneNumber': true };
    }
  }
}
