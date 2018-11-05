import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';

@Component({
  selector: 'app-change-email',
  templateUrl: './change-email.component.html',
  styleUrls: ['./change-email.component.scss'],
})
export class ChangeEmailComponent implements OnInit {

  public data = null;

  constructor(
    private modals: ModalService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
