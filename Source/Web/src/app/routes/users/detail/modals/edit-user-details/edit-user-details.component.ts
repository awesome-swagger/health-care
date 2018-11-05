import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../../modules/modals';

@Component({
  selector: 'app-edit-user-details',
  templateUrl: './edit-user-details.component.html',
  styleUrls: ['./edit-user-details.component.scss'],
})
export class EditUserDetailsComponent implements OnInit {

  public data = null;

  constructor(
    private modals: ModalService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
