import { Component, OnDestroy, OnInit } from '@angular/core';
import { groupBy as _groupBy, sumBy as _sumBy, uniqBy as _uniqBy, flattenDeep as _flattenDeep } from 'lodash';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { PopoverOptions } from '../../modules/popover';
import { AuthService, LocalStorageService, StoreService, UtilsService } from '../../services';
import { AddPlanComponent } from './modals/add-plan/add-plan.component';

@Component({
  selector: 'app-plans',
  templateUrl: './plans.component.html',
  styleUrls: ['./plans.component.scss'],
})
export class PlansComponent implements OnDestroy, OnInit {

  public organization = null;
  public facilities = [];
  public selectedFacility = null;
  public facilitiesOpen = false;
  public facilitiesDropOptions: PopoverOptions = {
    relativeTop: '48px',
    relativeRight: '0px',
  };
  public facilitiesFiltered = [];
  public averagesByCarePlan = null;
  public carePlanTemplates = [];
  public serviceAreas = [];
  public planTemplatesGrouped = [];
  public hideInactiveTemplates = true;

  public showServiceAreaHelp = false;
  public showCarePlanHelp = false;
  public showAveragesHelp = false;

  public accordionsOpen = [];

  private organizationSub = null;

  constructor(
    private modals: ModalService,
    private auth: AuthService,
    private local: LocalStorageService,
    private store: StoreService,
    public utils: UtilsService,
  ) { }

  public ngOnInit() {
    this.organizationSub = this.auth.organization$.subscribe((organization) => {
      if (organization === null) {
        return;
      }
      this.organization = organization;
      if (this.local.getObj('hide_inactive_plan_templates') === null) {
        this.hideInactiveTemplates = true;
      } else {
        this.hideInactiveTemplates = this.local.getObj('hide_inactive_plan_templates');
      }
      this.getFacilities(this.organization).then((facilities: any) => {
        this.facilities = facilities.filter((obj) => !obj.is_affiliate);
      });
      this.getPlansAverage(this.organization).then((plansAverage: any) => {
        this.averagesByCarePlan = plansAverage;
      });
      this.getPlanTemplates(this.organization).then((templates: any) => {
        this.getAllTemplateAverages(this.organization, templates).then((templatesWithAverages: any) => {
          this.carePlanTemplates = templatesWithAverages;
          this.serviceAreas = _uniqBy(this.carePlanTemplates.map((obj) => {
            return obj.service_area;
          }), (obj) => obj.id);
          let templatesGrouped = _groupBy(this.carePlanTemplates, (obj) => {
            return obj.service_area.id;
          });
          this.planTemplatesGrouped = Object.keys(templatesGrouped).map((key: any) => {
            return {
              serviceArea: key,
              serviceAreaObj: templatesGrouped[key][0].service_area,
              totalPatients: _sumBy(templatesGrouped[key], (o) => o.averages ? o.averages.total_patients : 0),
              templates: templatesGrouped[key].sort((a, b) => {
                if (a.name < b.name) { return -1; }
                if (a.name > b.name) { return 1; }
                return 0;
              }),
            };
          });
          this.planTemplatesGrouped.sort((a, b) => {
            if (a.serviceAreaObj.name < b.serviceAreaObj.name) { return -1; }
            if (a.serviceAreaObj.name > b.serviceAreaObj.name) { return 1; }
            return 0;
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
        organization_id: organization.id,
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

  public getPlansAverage(organization, facility = null) {
    let promise = new Promise((resolve, reject) => {
      let params = {
        patient__facility__organization: organization.id,
      };
      if (facility) {
        params['patient__facility'] = facility.id;
      }
      let plansAverage = this.store.CarePlan.listRoute('get', 'average', {}, params).subscribe(
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

  public getPlanTemplates(organization, facility = null) {
    let promise = new Promise((resolve, reject) => {
      let params = {
        care_plans__patient__facility__organization: organization.id,
      };
      if (facility) {
        params['care_plans__patient__facility'] = facility.id;
      }
      let templatesSub = this.store.CarePlanTemplate.readListPaged().subscribe(
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

  public getTemplateAverages(organization, template, facility = null) {
    let promise = new Promise((resolve, reject) => {
      let params = {
        care_plans__patient__facility__organization: organization.id,
      };
      if (facility) {
        params['care_plans__patient__facility'] = facility.id;
      }
      let averagesSub = this.store.CarePlanTemplate.detailRoute('get', template.id, 'average', {}, params).subscribe(
        (carePlanTemplateAverages) => {
          if (!carePlanTemplateAverages) {
            resolve({
              average_engagement: 0,
              average_outcome: 0,
              risk_level: 0,
              total_facilities: 0,
              total_patients: 0,
              time_count: 0,
              non_tcm_time_count: 0,
              time_allotted: 0,
            });
          } else {
            resolve(carePlanTemplateAverages);
          }
        },
        (err) => {
          resolve({
            average_engagement: 0,
            average_outcome: 0,
            risk_level: 0,
            total_facilities: 0,
            total_patients: 0,
            time_count: 0,
            non_tcm_time_count: 0,
            time_allotted: 0,
          });
        },
        () => {
          averagesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getAllTemplateAverages(organization, templates, facility = null) {
    let promise = new Promise((resolve, reject) => {
      let itemsProcessed = 0;
      if (templates.length === 0) {
        resolve(templates);
      }
      templates.forEach((item, index, array) => {
        this.getTemplateAverages(organization, item, facility).then((templateAverages) => {
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

  public toggleInactiveTemplates() {
    this.hideInactiveTemplates = !this.hideInactiveTemplates;
    this.local.setObj('hide_inactive_plan_templates', this.hideInactiveTemplates);
  }

  public filteredTemplates(templates) {
    if (this.hideInactiveTemplates) {
      return templates.filter((template) => {
        if (!template.averages) {
          return false;
        }
        return template.averages.total_patients > 0;
      });
    }
    return templates;
  }

  public totalCarePlans() {
    if (this.hideInactiveTemplates) {
      let templates = _flattenDeep(this.planTemplatesGrouped.map((obj) => obj.templates));
      let filteredTemplates = templates.filter((obj) => {
        if (!obj.averages) {
          return false;
        }
        return obj.averages.total_patients > 0;
      });
      return filteredTemplates.length;
    }
    return this.carePlanTemplates.length;
  }

  public totalServiceAreas() {
    if (this.hideInactiveTemplates) {
      return this.planTemplatesGrouped.filter((obj) => obj.totalPatients > 0).length;
    }
    return this.serviceAreas.length;
  }

  public zeroPad(num) {
    return num < 10 ? `0${num}` : `${num}`;
  }

  public formatTime(minutes) {
    if (!minutes) return '0:00';
    const h = `${Math.floor(minutes / 60)}`;
    const m = `${minutes % 60}`;
    return `${h}:${m.length === 1 ? '0' : ''}${minutes % 60}`
  }

  public totalTimeCount(templates, excludeTCM=false) {
    if (excludeTCM) {
      return _sumBy(templates, (obj) => obj.averages.non_tcm_time_count);
    } else {
      return _sumBy(templates, (obj) => obj.averages.time_count);
    }
  }

  public totalTimeAllotted(templates) {
    return _sumBy(templates, (obj) => obj.averages.time_allotted);
  }

  public templateTimeColor(template) {
    let totalTime = template.averages.non_tcm_time_count;
    let totalAllotted = template.averages.time_allotted;
    if (totalAllotted < 1) {
      return null;
    }
    return this.utils.timePillColor(totalTime, totalAllotted);
  }

  public serviceAreaTimeColor(templates) {
    let totalTime = this.totalTimeCount(templates, true);
    let totalAllotted = this.totalTimeAllotted(templates);
    if (totalAllotted < 1) {
      return null;
    }
    return this.utils.timePillColor(totalTime, totalAllotted);
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
    return Math.round(_sumBy(activeTemplates, (template) => template.averages.risk_level) / activeTemplates.length) || 0;
  }

  public addPlan(serviceAreaId = null) {
    let modalData = {
      duplicatePlan: null,
    };
    if (serviceAreaId) {
      modalData['serviceAreaId'] = serviceAreaId;
    }
    this.modals.open(AddPlanComponent, {
      closeDisabled: false,
      data: modalData,
      width: '480px',
    }).subscribe(() => {});
  }

  public duplicatePlan(plan) {
    this.modals.open(AddPlanComponent, {
      closeDisabled: false,
      data: {
        duplicatePlan: plan,
      },
      width: '480px',
    });
  }

  public setSelectedFacility(facility) {
    this.selectedFacility = facility;
    this.getPlansAverage(this.organization, this.selectedFacility).then((plansAverage: any) => {
      this.averagesByCarePlan = plansAverage;
    });
    this.getPlanTemplates(this.organization, this.selectedFacility).then((templates: any) => {
      this.getAllTemplateAverages(this.organization, templates, this.selectedFacility).then((templatesWithAverages: any) => {
        this.carePlanTemplates = templatesWithAverages;
        this.serviceAreas = _uniqBy(this.carePlanTemplates.map((obj) => {
          return obj.service_area;
        }), (obj) => obj.id);
        let templatesGrouped = _groupBy(this.carePlanTemplates, (obj) => {
          return obj.service_area.id;
        });
        this.planTemplatesGrouped = Object.keys(templatesGrouped).map((key: any) => {
          return {
            serviceArea: key,
            serviceAreaObj: templatesGrouped[key][0].service_area,
            totalPatients: _sumBy(templatesGrouped[key], (o) => o.averages ? o.averages.total_patients : 0),
            templates: templatesGrouped[key].sort((a, b) => {
              if (a.name < b.name) { return -1; }
              if (a.name > b.name) { return 1; }
              return 0;
            }),
          };
        });
        this.planTemplatesGrouped.sort((a, b) => {
          if (a.serviceAreaObj.name < b.serviceAreaObj.name) { return -1; }
          if (a.serviceAreaObj.name > b.serviceAreaObj.name) { return 1; }
          return 0;
        });
      });
    });
  }
}
