import { Component, OnDestroy, OnInit } from '@angular/core';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { PopoverOptions } from '../../modules/popover';
import { AuthService, StoreService } from '../../services';
import { AddPlanComponent } from './modals/add-plan/add-plan.component';
import { groupBy as _groupBy, sumBy as _sumBy } from 'lodash';

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

  public showServiceAreaHelp = false;
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
            return obj.service_area.id;
          });
          this.planTemplatesGrouped = Object.keys(templatesGrouped).map((key: any) => {
            return {
              serviceArea: key,
              serviceAreaObj: templatesGrouped[key][0].service_area,
              totalPatients: _sumBy(templatesGrouped[key], (o) => o.averages.total_patients),
              templates: templatesGrouped[key],
            };
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
