import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';

@Component({
  selector: 'app-preview-vital',
  templateUrl: './preview-vital.component.html',
  styleUrls: ['./preview-vital.component.scss'],
})
export class PreviewVitalComponent implements OnInit {

  public data = null;

  constructor(
    private modals: ModalService,
  ) {

  }

  public ngOnInit() {
  }

  public navigateBack() {
    this.modals.close({
      'next': this.data.from,
      'vital': this.data.vital,
    });
  }
}
