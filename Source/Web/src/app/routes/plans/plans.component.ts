import { Component, OnDestroy, OnInit } from '@angular/core';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { PopoverOptions } from '../../modules/popover';
import { AuthService, StoreService } from '../../services';
import { AddPlanComponent } from './modals/add-plan/add-plan.component';
import { groupBy as _groupBy } from 'lodash';

@Component({
  selector: 'app-plans',
  templateUrl: './plans.component.html',
  styleUrls: ['./plans.component.scss'],
})
export class PlansComponent implements OnDestroy, OnInit {

  public organization = null;
  public facilities = [];
  public facilitiesOpen = false;
  public facilitiesDropOptions: PopoverOptions = {};
  public facilitiesChecked: any = {};
  public facilitiesFiltered = [];
  public averagesByCarePlan = null;
  public carePlanTemplates = [];
  public planTemplatesGrouped = [];

  public showServiceLineHelp = false;
  public showCarePlanHelp = false;
  public showAveragesHelp = false;

  public accordionsOpen = [];

  private organizationSub = null;

  constructor(
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.organizationSub = this.auth.organization$.subscribe((organization) => {
      if (organization === null) {
        return;
      }
      this.organization = organization;
      this.getFacilities(this.organization).then((facilities: any) => {
        this.facilities = facilities;
        this.getPlansAverage(this.organization).then((plansAverage: any) => {
          this.averagesByCarePlan = plansAverage;
        });
      });
      this.getPlanTemplates(this.organization).then((templates: any) => {
        this.getAllTemplateAverages(this.organization, templates).then((templatesWithAverages: any) => {
          this.carePlanTemplates = templatesWithAverages;
          let templatesGrouped = _groupBy(this.carePlanTemplates, (obj) => {
            return obj.type.id;
          });
          this.planTemplatesGrouped = Object.keys(templatesGrouped).map((key: any) => {
            return {type: key, typeObj: templatesGrouped[key][0].type, templates: templatesGrouped[key]};
          });
        });
      });
    });
  }

  public ngOnDestroy() {
    if (this.organizationSub) {
      this.organizationSub.unsubscribe();
    }
  }

  public getFacilities(organization) {
    let promise = new Promise((resolve, reject) => {
      let facilitiesSub = this.store.Facility.readListPaged({
        organization: organization.id,
      }).subscribe(
        (facilities) => {
          resolve(facilities);
        },
        (err) => {
          reject(err);
        },
        () => {
          facilitiesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getPlansAverage(organization) {
    let promise = new Promise((resolve, reject) => {
      let plansAverage = this.store.CarePlan.listRoute('get', 'average', {}, {
        patient__facility__organization: organization.id,
      }).subscribe(
        (plansAverage) => {
          resolve(plansAverage);
        },
        (err) => {
          reject(err);
        },
        () => {
          plansAverage.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getPlanTemplates(organization) {
    let promise = new Promise((resolve, reject) => {
      let templatesSub = this.store.CarePlanTemplate.readListPaged({
        // care_plans__patient__facility__organization: organization.id,
      }).subscribe(
        (carePlanTemplates) => {
          resolve(carePlanTemplates);
        },
        (err) => {},
        () => {
          templatesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getTemplateAverages(organization, template) {
    let promise = new Promise((resolve, reject) => {
      let averagesSub = this.store.CarePlanTemplate.detailRoute('get', template.id, 'average', {}, {
        care_plans__patient__facility__organization: organization.id,
      }).subscribe(
        (carePlanTemplateAverages) => {
          resolve(carePlanTemplateAverages);
        },
        (err) => {
          reject(err);
        },
        () => {
          averagesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getAllTemplateAverages(organization, templates) {
    let promise = new Promise((resolve, reject) => {
      let itemsProcessed = 0;
      templates.forEach((item, index, array) => {
        this.getTemplateAverages(organization, item).then((templateAverages) => {
          item.averages = templateAverages;
          itemsProcessed++;
          if (itemsProcessed === array.length) {
            resolve(templates);
          }
        }).catch((err) => {
          reject(err);
        });
      });
    });
    return promise;
  }

  public addPlan() {
    this.modals.open(AddPlanComponent, {
      closeDisabled: true,
      data: {
        duplicating: false,
      },
      width: '480px',
    }).subscribe(() => {});
  }

  public duplicatePlan() {
    this.modals.open(AddPlanComponent, {
      closeDisabled: true,
      data: {
        duplicating: true,
      },
      width: '480px',
    });
  }

  public copyPlan() {
    this.modals.open(AddPlanComponent, {
      closeDisabled: true,
      width: '480px',
    }).subscribe(() => {});
  }

  public clickCheckAllFacilities() {
    this.facilitiesChecked = {};
    this.facilities.map((obj) => {
      this.facilitiesChecked[obj.id] = true;
    });
    this.applyFacilityFilter();
  }

  public clickUncheckAllFacilities() {
    this.facilitiesChecked = {};
    this.applyFacilityFilter();
  }

  public applyFacilityFilter() {
    this.facilitiesFiltered = Object.keys(this.facilitiesChecked);
  }
}
