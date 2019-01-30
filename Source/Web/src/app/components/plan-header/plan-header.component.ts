import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as moment from 'moment';
import { ModalService } from '../../modules/modals';
import { PlanDurationComponent } from '../../components/modals/plan-duration/plan-duration.component';
import { AuthService, StoreService, UtilsService } from '../../services';

@Component({
  selector: 'app-plan-header',
  templateUrl: './plan-header.component.html',
  styleUrls: ['./plan-header.component.scss']
})
export class PlanHeaderComponent implements OnInit, OnDestroy {

  public moment = moment;
  private _planTemplate = null;
  private organization = null;
  public editName = false;
  public newPlanName = '';
  public carePlanAverage = null;

  public openReassignPatients;
  public addPlan;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
    public utils: UtilsService,
  ) {
    let paramSub = this.route.params.subscribe(
      (params) => {
        let orgSub = this.auth.organization$.subscribe(
          (organization) => {
            if (organization === null) {
              return;
            }
            this.organization = organization;
            this.getAverages(this.organization, params.id).then((carePlanAverage) => {
              this.carePlanAverage = carePlanAverage;
            }).catch((e) => {
              this.carePlanAverage = null;
            });
          },
          (err) => {},
          () => {
            orgSub.unsubscribe();
          },
        );
      },
      (err) => {},
      () => {},
    );
  }

  public ngOnInit() { }

  public ngOnDestroy() { }

  public clickEditName() {
    this.editName = true;
    this.newPlanName = this.planTemplate.name;
  }

  public cancelEditName() {
    this.editName = false;
  }

  public saveEditName() {
    this.store.CarePlanTemplate.update(this.planTemplate.id, {
      name: this.newPlanName,
    }, true).subscribe(
      (data) => {
        this.planTemplate.name = this.newPlanName;
        this.newPlanName = '';
        this.editName = false;
      },
      (err) => {},
      () => {}
    );
  }

  public openPlanDuration() {
    let modalSub = this.modals.open(PlanDurationComponent, {
      closeDisabled: true,
      data: {
        planTemplate: this.planTemplate,
        numPatients: this.carePlanAverage ? this.carePlanAverage.total_patients : 0,
      },
      width: '384px',
    }).subscribe(
      (data) => {
        console.log(data);
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public getAverages(organization, planId) {
    let promise = new Promise((resolve, reject) => {
      let averagesSub = this.store.CarePlanTemplate.detailRoute('get', planId, 'average', {}, {
        care_plans__patient__facility__organization: organization.id,
      }).subscribe(
        (carePlanAverage) => {
          resolve(carePlanAverage);
        },
        (err) => {
          reject(err);
        },
        () => {
          averagesSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  @Input()
  public get planTemplate() {
    return this._planTemplate;
  }

  public set planTemplate(value) {
    this._planTemplate = value;
  }

  public getPillColor(percentage) {
    if (percentage >= 90) {
      return '#4caf50';
    } else if (percentage <= 89 && percentage >= 70) {
      return '#ff9800';
    } else if (percentage <= 69 && percentage >= 50) {
       return '#ca2c4e';
    } else {
      return '#880e4f';
    }
  }
}
