import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService } from '../../../../modules/modals';
import { AuthService, StoreService } from '../../../../services';

@Component({
  selector: 'app-delete-plan',
  templateUrl: './delete-plan.component.html',
  styleUrls: ['./delete-plan.component.scss']
})
export class DeletePlanComponent implements OnInit, OnDestroy {

  public data = null;
  public facilities = [];
  public planTemplates = [];
  public practitioners = [];
  public accordianStatuses = {};
  public bulkReassign = {};
  public bulkManager = {};
  public bulkNewPlan = {};
  public bulkInactive = {};
  public otherPlansInfoOpen = {};
  public otherPlansOpen = {};

  private facilitiesSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    this.getQualifiedPractitioners().then((practitioners: any) => {
      this.practitioners = practitioners;
    });
    this.getCarePlanTemplates().then((planTemplates: any) => {
      this.planTemplates = planTemplates.filter((obj) => obj.id !== this.data.planTemplate.id);
    });
    this.facilitiesSub = this.auth.facilities$.subscribe((facilities) => {
      if (!facilities) {
        return;
      }
      this.facilities = facilities.filter((obj) => {
        return !obj.is_affiliate;
      }).slice();
      this.facilities.forEach((facility) => {
        this.getPlansForTemplate(facility.id, this.data.planTemplate.id).then((plans: any) => {
          if (this.data.plan) {
            facility.planInstances = plans.results.filter((obj) => obj.id === this.data.plan.id);
          } else {
            facility.planInstances = plans.results;
          }
        }).catch((err) => {
          facility.planInstances = [];
        });
      });
    });
  }

  public ngOnDestroy() {
    if (this.facilitiesSub) {
      this.facilitiesSub.unsubscribe();
    }
  }

  public getCarePlanTemplates() {
    let promise = new Promise((resolve, reject) => {
      let plansSub = this.store.CarePlanTemplate.readListPaged().subscribe(
        (plans) => resolve(plans),
        (err) => reject(err),
        () => {
          plansSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getPlansForTemplate(facilityId, templateId) {
    let promise = new Promise((resolve, reject) => {
      let plansSub = this.store.Facility.detailRoute('get', facilityId, 'care_plan_templates/' + templateId + '/care_plans').subscribe(
        (plans) => resolve(plans),
        (err) => reject(err),
        () => {
          plansSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public getQualifiedPractitioners() {
    let promise = new Promise((resolve, reject) => {
      let employeeSub = this.store.EmployeeProfile.readListPaged({
        // TODO: Get only qualified practitioners
      }).subscribe(
        (employees) => resolve(employees),
        (err) => reject(err),
        () => {
          employeeSub.unsubscribe();
        }
      )
    });
    return promise;
  }

  public clickClose() {
    this.modals.close(null);
  }

  public saveDisabled() {
    if (!this.facilities) {
      return true;
    }
    let disabled = false;
    this.facilities.forEach((facility) => {
      if (this.bulkReassign[facility.id]) {
        if (this.bulkInactive[facility.id]) {
          return;
        }
        if (!this.bulkNewPlan[facility.id] || !this.bulkManager[facility.id]) {
          disabled = true;
        }
      } else {
        if (!facility.planInstances || facility.planInstances.length < 1) {
          return;
        }
        facility.planInstances.forEach((planInstance) => {
          if (planInstance.selectedInactive) {
            return;
          }
          if (!planInstance.selectedNewPlan || !planInstance.selectedCM) {
            disabled = true;
          }
        });
      }
    });
    return disabled;
  }

  public clickSave() {
    this.facilities.forEach((facility) => {
      if (!facility.planInstances || facility.planInstances.length < 1) {
        return;
      }
      if (this.bulkReassign[facility.id]) {
        let payload = facility.planInstances.map((obj) => {
          return {
            plan: obj.id,
            plan_template: this.bulkNewPlan[facility.id],
            care_manager: this.bulkManager[facility.id],
            inactive: this.bulkInactive[facility.id],
          }
        });
        let reassignSub = this.store.CarePlanTemplate.listRoute('post', 'bulk_reassign_plan', payload).subscribe(
          (success) => {
            this.modals.close('success');
          },
          (err) => {
            this.modals.close('error');
          },
          () => {
            reassignSub.unsubscribe();
          }
        );
      } else {
        let payload = facility.planInstances.map((obj) => {
          return {
            plan: obj.id,
            plan_template: obj.selectedNewPlan,
            care_manager: obj.selectedCM,
            inactive: obj.selectedInactive,
          }
        });
        let reassignSub = this.store.CarePlanTemplate.listRoute('post', 'bulk_reassign_plan', payload).subscribe(
          (success) => {
            this.modals.close('success');
          },
          (err) => {
            this.modals.close('error');
          },
          () => {
            reassignSub.unsubscribe();
          }
        );
      }
    });
  }
}
