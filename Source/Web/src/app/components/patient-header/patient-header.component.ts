import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { StoreService } from '../../services';

@Component({
  selector: 'app-patient-header',
  templateUrl: './patient-header.component.html',
  styleUrls: ['./patient-header.component.scss']
})
export class PatientHeaderComponent implements OnInit, OnDestroy {

  private _patient = null;

  constructor(
    private store: StoreService,
  ) { }

  public ngOnInit() { }

  public ngOnDestroy() { }

  @Input()
  public get patient() {
    return this._patient;
  }

  public set patient(value) {
    this._patient = value;
    if (this._patient) {
      let carePlansSub = this.store.CarePlan.readListPaged({
        patient: this._patient.id,
      }).subscribe(
        (data) => {
          console.log(data);
        },
        (err) => {},
        () => {
          carePlansSub.unsubscribe();
        },
      );
    }
  }
}
