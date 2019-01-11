import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StoreService } from '../../services';
import { find as _find } from 'lodash';

@Component({
  selector: 'app-patient-header',
  templateUrl: './patient-header.component.html',
  styleUrls: ['./patient-header.component.scss']
})
export class PatientHeaderComponent implements OnInit, OnDestroy {

  private _patient = null;
  public plans = null;
  public currentPlanId = null;
  public patientId = null;
  public currentPlan = null;

  public teamListOpen;
  public openProblemAreas;
  public openFinancialDetails;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe(params => {

      let carePlanSub = this.store.PatientCarePlans(params.patientId).read().subscribe(
        data => {
          this.plans = data;
          this.currentPlan = _find(data, p => p.id === params.planId);
        },
        err => {},
        () => carePlanSub.unsubscribe()
      )

      this.currentPlanId = params.planId;
      this.patientId = params.patientId;
    })
  }

  public ngOnDestroy() { }

  @Input()
  public get patient() {
    return this._patient;
  }

  public set patient(value) {
    this._patient = value;
  }
}
