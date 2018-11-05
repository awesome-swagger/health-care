import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import * as moment from 'moment';
import { AuthService, StoreService } from '../../services';

@Component({
  selector: 'app-plan-header',
  templateUrl: './plan-header.component.html',
  styleUrls: ['./plan-header.component.scss']
})
export class PlanHeaderComponent implements OnInit, OnDestroy {

  public moment = moment;
  private _planTemplate = null;
  private organization = null;
  public carePlanAverage = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private auth: AuthService,
    private store: StoreService,
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
}
