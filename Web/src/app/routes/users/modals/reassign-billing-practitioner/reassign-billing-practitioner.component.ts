import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
  groupBy as _groupBy,
  uniqBy as _uniqBy,
} from 'lodash';
import { ModalService } from '../../../../modules/modals';
import { AuthService, StoreService } from '../../../../services';
import { Utils } from '../../../../utils';

@Component({
  selector: 'app-reassign-billing-practitioner',
  templateUrl: './reassign-billing-practitioner.component.html',
  styleUrls: ['./reassign-billing-practitioner.component.scss']
})
export class ReassignBillingPractitionerComponent implements OnInit {

  public objectKeys = Object.keys;

  public data = null;

  public plans = [];
  public plansGrouped = null;
  public practitioners = [];

  public accordianStatuses = [];
  public bulkReassign = [];
  public bulkNewPlan = [];
  public bulkManager = [];
  public bulkPractitioner = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.getPlansForBillingPractitioner(this.data.billingPractitioner).then((plans: any) => {
      this.plans = plans.map((obj) => {
        obj.selectedBP = obj.billing_practitioner.id;
      });
      this.plansGrouped = this.groupByFacility(plans);
      this.getQualifiedPractitioners().then((practitioners: any) => {
        this.practitioners = practitioners;
      });
    });
  }

  public getPlansForBillingPractitioner(bpId) {
    let promise = new Promise((resolve, reject) => {
      let plansSub = this.store.CarePlan.readListPaged({
        billing_practitioner: bpId
      }).subscribe(
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

  public groupByFacility(plans) {
    return _groupBy(plans, (obj) => {
      return obj.patient.facility.id;
    });
  }

  public clickCancel() {
    this.modals.close(null);
  }

  public clickSave() {
    // For each facility, if reassign in bulk is checked then make one post request with all the care plans included
    // If reassign in bulk is not checked then make a post request with all the care plans included, but with the selected billing practitioner for each
    Object.keys(this.plansGrouped).forEach((facilityId) => {
      if (this.bulkReassign[facilityId]) {
        let payload = this.plansGrouped[facilityId].map((obj) => {
          return {
            id: obj.id,
            billing_practitioner: this.bulkPractitioner[facilityId]
          }
        });
        let reassignSub = this.store.CarePlan.listRoute('post', 'bulk_reassign_billing_practitioner', payload).subscribe(
          (success) => {
            Utils.logDebug('success', success);
          },
          (err) => {
            Utils.logError('failed to reassign billing practitioners', err, payload);
          },
          () => {
            reassignSub.unsubscribe();
          }
        );
      } else {
        let payload = this.plansGrouped[facilityId].map((obj) => {
          return {
            id: obj.id,
            billing_practitioner: obj.selectedBP,
          }
        });
        let reassignSub = this.store.CarePlan.listRoute('post', 'bulk_reassign_billing_practitioner', payload).subscribe(
          (success) => {
            Utils.logDebug('success', success);
          },
          (err) => {
            Utils.logError('failed to reassign billing practitioners', err, payload);
          },
          () => {
            reassignSub.unsubscribe();
          }
        );
      }
    });
  }
}
