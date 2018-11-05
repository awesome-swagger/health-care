import { browser, element, by } from 'protractor';

export class AppPage {
  navigateTo() {
    return browser.get('/');
  }

  getOpenModalButton() {
    return element(by.cssContainingText('button', 'Open Modal'));
  }

  getConfirmModal() {
    return element(by.tagName('app-modal-confirm'));
  }

  getConfirmModalYesButton() {
    return this.getConfirmModal().element(by.css('.button--green'));
  }

  getResultToast() {
    return element(by.css('.toast__text'));
  }
}
