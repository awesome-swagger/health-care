import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-delete-plan',
  templateUrl: './delete-plan.component.html',
  styleUrls: ['./delete-plan.component.scss']
})
export class DeletePlanComponent implements OnInit {

  public data = null;
  public facilities = [
    {
      name: 'Mountain View',
      patients: [
        {
          name: 'Cori Soderman',
        },
        {
          name: 'Theresa Beckstrom',
        },
        {
          name: 'Giovanni Manuel',
        },
        {
          name: 'Harold Taylor',
        },
      ]
    },
    {
      name: 'South Ogden Family Medicine',
      patients: [
        {
          name: 'Cori Soderman',
        },
        {
          name: 'Theresa Beckstrom',
        },
      ]
    }
  ]
  public accordianStatuses = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    // Get all patient's on the plan
    // group patient's by facility
    // wire up "reassign in bulk" for each facility
    // for each facility, if reassign in bulk is clicked send one post request with all patients having the same data
    // if reassign in bulk is not clicked, send a post request for each patient with different data.
    this.accordianStatuses = new Array(this.facilities.length).fill(false);
    this.getPlansForTemplate(this.data.planTemplate.id).then((plans: any) => {
      console.log(plans);
    });
  }

  public getPlansForTemplate(templateId) {
    let promise = new Promise((resolve, reject) => {
      let planTemplatesSub = this.store.CarePlan.readListPaged({
        plan_template: templateId
      }).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          planTemplatesSub.unsubscribe();
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
    // return _groupBy(plans, (obj) => {
    //   return obj.patient.facility.id;
    // });
  }

  public close() {
    this.modals.close(null);
  }

}
