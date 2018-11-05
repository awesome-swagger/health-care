import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StoreService, NavbarService } from '../../../services';

@Component({
  selector: 'app-patient-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class PatientDashboardComponent implements OnDestroy, OnInit {

  public patient = null;

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
      this.nav.patientDetailState(params.id);
      this.store.PatientProfile.read(params.id).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        },
        (err) => {},
        () => {},
      );
    });
  }

  public ngOnDestroy() { }
}
