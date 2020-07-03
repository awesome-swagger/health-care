import { Component } from '@angular/core';
import { ModalService } from '../modal.service';

@Component({
  selector: 'app-modal-confirm',
  templateUrl: './confirm.modal.html',
  styleUrls: ['./confirm.modal.scss']
})
export class ConfirmModalComponent {

  public data;

  public dataDefaults: {} = {
    title: 'Are You Sure?',
    body: 'Please confirm your choice.',
    okText: 'Confirm',
    cancelText: 'Cancel',
  };

  constructor(public modal: ModalService) {
    this.data = Object.assign({}, this.dataDefaults, this.data);
  }
}
