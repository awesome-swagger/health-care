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

  private facilitiesSub = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    this.accordianStatuses = new Array(this.facilities.length).fill(false);
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
      this.facilities = facilities.filter((obj) => !obj.is_affiliate);
      this.facilities.forEach((facility) => {
        this.accordianStatuses[facility.id] = true;
        this.getPlansForTemplate(facility.id, this.data.planTemplate.id).then((plans: any) => {
          facility.plans = plans.results;
        }).catch((err) => {
          facility.plans = [];
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

  public clickSave() {
    this.facilities.forEach((facility) => {
      if (!facility.plans || facility.plans.length < 1) {
        return;
      }
      if (this.bulkReassign[facility.id]) {
        let payload = facility.plans.map((obj) => {
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
        let payload = facility.plans.map((obj) => {
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
