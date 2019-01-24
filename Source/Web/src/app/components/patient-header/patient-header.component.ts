import { Component, EventEmitter, Input, Output, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService } from '../../modules/modals';
import { ToastService } from '../../modules/toast';
import { StoreService } from '../../services';
import { find as _find } from 'lodash';
import { ProblemAreasComponent } from '../../routes/patient/modals/problem-areas/problem-areas.component';

@Component({
  selector: 'app-patient-header',
  templateUrl: './patient-header.component.html',
  styleUrls: ['./patient-header.component.scss']
})
export class PatientHeaderComponent implements OnInit, OnDestroy {

  public _currentPage = null;
  public patient = null;
  public selectedPlan = null;
  public carePlans = [];
  public careTeamMembers = [];
  public careManager = null;
  public problemAreas = [];

  @Output()
  public onPlanChange = new EventEmitter<any>();

  public teamListOpen;
  public openFinancialDetails;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private toast: ToastService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe(
      (params) => {
        this.fetchPatient(params.patientId).then(
          (patient: any) => {
            this.patient = patient;
            this.fetchCarePlans(params.patientId).then(
              (carePlans: any) => {
                this.carePlans = carePlans;
                this.selectedPlan = carePlans.find((obj) => {
                  return obj.id === params.planId;
                });
              },
              (err) => {
                this.toast.error('Error fetching care plans');
                console.log(err);
              },
            )
          },
          (err) => {
            this.toast.error('Error fetching patient');
            console.log(err);
          }
        );
        this.fetchCareTeamMembers(params.planId).then(
          (teamMembers: any) => {
            this.careTeamMembers = teamMembers.filter((obj) => {
              return !obj.is_manager;
            });
            this.careManager = teamMembers.filter((obj) => {
              return obj.is_manager;
            })[0];
          },
          (err) => {
            this.toast.error('Error fetching care team members');
            console.log(err);
          },
        );
        this.fetchProblemAreas(params.patientId).then(
          (problemAreas: any) => {
            this.problemAreas = problemAreas;
          },
          (err) => {
            this.toast.error('Error fetching problem areas');
            console.log(err);
          }
        );
      }
    );
  }

  public ngOnDestroy() { }

  public fetchPatient(patientId) {
    let promise = new Promise((resolve, reject) => {
      let fetchSub = this.store.PatientProfile.read(patientId).subscribe(
        (patient) => resolve(patient),
        (err) => reject(err),
        () => {
          fetchSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public fetchCarePlans(patientId) {
    let promise = new Promise((resolve, reject) => {
      let carePlansSub = this.store.CarePlan.readListPaged({
        patient: patientId,
      }).subscribe(
        (carePlans) => resolve(carePlans),
        (err) => reject(err),
        () => {
          carePlansSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public fetchCareTeamMembers(planId) {
    let promise = new Promise((resolve, reject) => {
      let teamMembersSub = this.store.CarePlan.detailRoute('get', planId, 'care_team_members').subscribe(
        (teamMembers) => resolve(teamMembers),
        (err) => reject(err),
        () => {
          teamMembersSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public fetchProblemAreas(patient) {
    let promise = new Promise((resolve, reject) => {
      let problemAreasSub = this.store.ProblemArea.readListPaged({
        patient: patient,
      }).subscribe(
        (problemAreas) => resolve(problemAreas),
        (err) => reject(err),
        () => {
          problemAreasSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public changeSelectedPlan(plan) {
    this.router.navigate(['/patient', this.patient.id, this.currentPage, plan.id]);
  }

  public openProblemAreas() {
    this.modals.open(ProblemAreasComponent, {
      closeDisabled: true,
      data: {
        patient: this.patient,
        problemAreas: this.problemAreas,
      },
      width: '560px',
    });
  }

  @Input()
  public get currentPage() {
    return this._currentPage;
  }

  public set currentPage(value) {
    this._currentPage = value;
  }
}
