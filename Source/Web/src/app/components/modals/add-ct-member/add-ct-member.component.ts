import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-add-ct-member',
  templateUrl: './add-ct-member.component.html',
  styleUrls: ['./add-ct-member.component.scss'],
})
export class AddCTMemberComponent implements OnInit {

  public data = null;
  public selectedProvider = null;
  public availableProviders = [];

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.fetchAvailableProviders().then((providers: any) => {
      this.availableProviders = providers;
    });
  }

  public fetchAvailableProviders() {
    let promise = new Promise((resolve, reject) => {
      // If adding a care manager fetch only care managers
      if (this.data.is_manager) {
        let fetchSub = this.store.EmployeeProfile.readListPaged().subscribe(
          (managers) => resolve(managers),
          (err) => reject(err),
          () => {
            fetchSub.unsubscribe();
          }
        );
      }
      // If adding a specific role fetch only employees who match that role
      if (this.data.role) {
        let fetchSub = this.store.EmployeeProfile.readListPaged({
          role_id: this.data.role.id,
        }).subscribe(
          (providers) => resolve(providers),
          (err) => reject(err),
          () => {
            fetchSub.unsubscribe();
          },
        );
      }
    });
    return promise;
  }

  public selectProvider(provider) {
    this.selectedProvider = provider;
  }

  public clickSave() {
    this.modal.close(this.selectedProvider);
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
