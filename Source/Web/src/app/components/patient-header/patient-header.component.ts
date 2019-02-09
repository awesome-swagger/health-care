import { Component, EventEmitter, Input, Output, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { find as _find } from 'lodash';
import * as moment from 'moment';
import { ModalService } from '../../modules/modals';
import { ToastService } from '../../modules/toast';
import { PopoverOptions } from '../../modules/popover';
import { StoreService, UtilsService } from '../../services';
import { ProblemAreasComponent } from '../../routes/patient/modals/problem-areas/problem-areas.component';

@Component({
  selector: 'app-patient-header',
  templateUrl: './patient-header.component.html',
  styleUrls: ['./patient-header.component.scss']
})
export class PatientHeaderComponent implements OnInit, OnDestroy {

  public _currentPage = null;
  public patient = null;
  public patientPlansOverview = null;
  public selectedPlan = null;
  public selectedPlanOverview = null;
  public carePlans = [];
  public careTeamMembers = [];
  public careManager = null;
  public problemAreas = [];

  @Output()
  public onPlanChange = new EventEmitter<any>();

  public planSelectOpen = false;
  public teamListOpen = false;
  public openFinancialDetails;

  public planSelectOptions: PopoverOptions = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private toast: ToastService,
    private store: StoreService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe(
      (params) => {
        this.getPatient(params.patientId).then(
          (patient: any) => {
            this.patient = patient;
            let overviewSub = this.store.PatientProfile.detailRoute('get', this.patient.id, 'care_plan_overview').subscribe(
              (overview: any) => {
                this.patientPlansOverview = overview.results;
                this.getCarePlans(params.patientId).then(
                  (carePlans: any) => {
                    this.carePlans = carePlans;
                    this.selectedPlan = carePlans.find((obj) => {
                      return obj.id === params.planId;
                    });
                    this.selectedPlanOverview = this.getOverviewForPlanTemplate(this.selectedPlan.plan_template.id);
                  },
                  (err) => {
                    this.toast.error('Error fetching care plans');
                    console.log(err);
                  },
                );
              },
              (err) => {},
              () => {
                overviewSub.unsubscribe();
              },
            );
          },
          (err) => {
            this.toast.error('Error fetching patient');
            console.log(err);
          }
        );
        this.getCareTeamMembers(params.planId).then(
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
        this.getProblemAreas(params.patientId).then(
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

  public getPatient(patientId) {
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

  public getCarePlans(patientId) {
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

  public getCareTeamMembers(planId) {
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

  public getProblemAreas(patient) {
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

  public getOverviewForPlanTemplate(planTemplateId) {
    return this.patientPlansOverview.find((obj) => obj.plan_template.id === planTemplateId);
  }

  public changeSelectedPlan(plan) {
    this.router.navigate(['/patient', this.patient.id, this.currentPage, plan.id]);
  }

  public routeToPatientHistory() {
    this.router.navigate(['/patient', this.patient.id, 'history', this.selectedPlan.id]);
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
