import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-plan-duration',
  templateUrl: './plan-duration.component.html',
  styleUrls: ['./plan-duration.component.scss'],
})
export class PlanDurationComponent implements OnInit {

  public data = null;
  public planTemplate = null;
  public numPatients = 0;
  // Choice between "onGoing" and "numWeeks"
  public radioChoice = 'onGoing';
  public weeksInput = 1;

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    if (this.data) {
      this.planTemplate = this.data.planTemplate ? this.data.planTemplate : null;
      this.numPatients = this.data.numPatients ? this.data.numPatients : 0;
      if (this.planTemplate.duration_weeks >= 0) {
        this.radioChoice = 'numWeeks';
      }
      this.weeksInput = this.planTemplate.duration_weeks;
    }
  }


  public cancel() {
    this.modals.close(null);
  }

  public save() {
    let duration = this.radioChoice === 'onGoing' ? -1 : this.weeksInput;
    this.store.CarePlanTemplate.update(this.planTemplate.id, {
      duration_weeks: duration,
    }, true).subscribe(
      (data) => {
        this.planTemplate.duration_weeks = duration;
        this.modals.close(null);
      },
      (err) => {},
      () => {}
    );
  }
}
