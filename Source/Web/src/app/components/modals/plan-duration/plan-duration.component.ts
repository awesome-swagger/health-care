import { Component, OnInit } from '@angular/core';
import { ModalService, } from '../../../modules/modals';

@Component({
  selector: 'app-plan-duration',
  templateUrl: './plan-duration.component.html',
  styleUrls: ['./plan-duration.component.scss'],
})
export class PlanDurationComponent implements OnInit {

  public data = null;

  constructor(
    private modals: ModalService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
  }

  public close() {
    this.modals.close(null);
  }
}
