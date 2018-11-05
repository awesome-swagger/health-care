import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss'],
})
export class ChangePasswordComponent implements OnInit {

  public data = null;

  constructor(
    private modals: ModalService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
