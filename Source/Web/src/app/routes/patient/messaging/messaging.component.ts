import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-patient-messaging',
  templateUrl: './messaging.component.html',
  styleUrls: ['./messaging.component.scss'],
})
export class PatientMessagingComponent implements OnDestroy, OnInit {

  public patient = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: StoreService,
    private nav: NavbarService,
  ) { }


  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.id, params.planId);
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
