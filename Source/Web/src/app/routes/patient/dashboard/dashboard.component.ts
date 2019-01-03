import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StoreService, NavbarService } from '../../../services';
import { PercentageGaugeComponent } from '../../../components/graphs/percentage-gauge/percentage-gauge.component'
import { ResultsGraphComponent } from '../../../components/graphs/results-graph/results-graph.component';

@Component({
  selector: 'app-patient-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class PatientDashboardComponent implements OnDestroy, OnInit {

  public patient = null;
  public carePlans = null;

  public datepickerOptions = {
     relativeTop: '-368px',
   };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId);
      this.getPatient(params.patientId).then((patient) => {
        this.patient = patient;
        this.nav.addRecentPatient(this.patient);
      });
      this.getCarePlans(params.patientId).then((plans) => {
        this.carePlans = plans;
      });
    });
  }

  public getPatient(patientId) {
    return new Promise((resolve, reject) => {
        let patientSub = this.store.PatientProfile.read(patientId).subscribe(
          patient => resolve(patient),
          err => reject(err),
          () => patientSub.unsubscribe()
        )
    });
  }

  public getCarePlans(patientId) {
    return new Promise((resolve, reject) => {
        let carePlanSub = this.store.PatientCarePlans(patientId).read().subscribe(
          plans => resolve(plans),
          err => reject(err),
          () => carePlanSub.unsubscribe()
        )
    });
  } 

  public ngOnDestroy() { }
}
