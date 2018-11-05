import { AppPage } from './app.po';

describe('startstudio-angular-template App', function() {
  let page: AppPage;

  beforeEach(() => {
    page = new AppPage();
  });

  it('should open a confirm modal when open modal button is clicked', () => {
    page.navigateTo();
    page.getOpenModalButton().click();
    expect(page.getConfirmModal().isPresent);
  });

  it('should create a toast when the user clicks on yes', () => {
    page.navigateTo();
    page.getOpenModalButton().click().then(() => {
      page.getConfirmModalYesButton().click().then(() => {
        expect(page.getResultToast().getText()).toEqual('Clicked Yes');
      });
    });
  });
});
