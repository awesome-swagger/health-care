import { Component, OnDestroy, OnInit } from '@angular/core';
import { groupBy as _groupBy, sumBy as _sumBy } from 'lodash';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { PopoverOptions } from '../../modules/popover';
import { AuthService, StoreService, UtilsService } from '../../services';
import { AddPlanComponent } from './modals/add-plan/add-plan.component';

@Component({
  selector: 'app-plans',
  templateUrl: './plans.component.html',
  styleUrls: ['./plans.component.scss'],
})
export class PlansComponent implements OnDestroy, OnInit {

  public organization = null;
  public facilities = [];
  public facilitiesOpen = false;
  public facilitiesDropOptions: PopoverOptions = {
    relativeTop: '48px',
    relativeRight: '0px',
  };
  public facilitiesChecked: any = {};
  public facilitiesFiltered = [];
  public averagesByCarePlan = null;
  public carePlanTemplates = [];
  public serviceAreas = [];
  public planTemplatesGrouped = [];

  public showServiceAreaHelp = false;
  public showCarePlanHelp = false;
  public showAveragesHelp = false;

  public accordionsOpen = [];

  private organizationSub = null;

  public toolCPOpen;

  public fetchPlanTemplates;

  constructor(
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
    public utils: UtilsService,
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
          this.serviceAreas = this.carePlanTemplates.map((obj) => {
            return obj.service_area;
          });
          let templatesGrouped = _groupBy(this.carePlanTemplates, (obj) => {
            return obj.service_area.id;
          });
          this.planTemplatesGrouped = Object.keys(templatesGrouped).map((key: any) => {
            return {
              serviceArea: key,
              serviceAreaObj: templatesGrouped[key][0].service_area,
              totalPatients: _sumBy(templatesGrouped[key], (o) => o.averages ? o.averages.total_patients : 0),
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
          resolve({
            average_engagement: 0,
            average_outcome: 0,
            risk_level: 0,
            total_facilities: 0,
            total_patients: 0,
          });
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

  public zeroPad(num) {
    return num < 10 ? `0${num}` : `${num}`;
  }

  public totalTimeCount(templates) {
    let hours = 0;
    let minutes = 0;
    templates.forEach((obj) => {
      if (!obj.averages.time_count) {
        return;
      }
      let timeCountSplit = obj.averages.time_count.split(":");
      let splitHours = parseInt(timeCountSplit[0]);
      let splitMinutes = parseInt(timeCountSplit[1]);
      hours += splitHours;
      minutes += splitMinutes;
    });
    hours += Math.floor((minutes / 60));
    minutes = minutes % 60;
    return `${hours}:${this.zeroPad(minutes)}`;
  }

  public addPlan() {
    this.modals.open(AddPlanComponent, {
      closeDisabled: false,
      data: {
        duplicating: false,
      },
      width: '480px',
    }).subscribe(() => {});
  }

  public duplicatePlan() {
    this.modals.open(AddPlanComponent, {
      closeDisabled: false,
      data: {
        duplicating: true,
      },
      width: '480px',
    });
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

  public totalRiskLevel(templates) {
    if (!templates || templates.length === 0) {
      return 0;
    }
    let activeTemplates = templates.filter((obj) => {
      if (!obj.averages) {
        return false;
      }
      return obj.averages.total_patients > 0;
    });
    return (_sumBy(activeTemplates, (template) => template.averages.risk_level) / activeTemplates.length) || 0;
  }
}
