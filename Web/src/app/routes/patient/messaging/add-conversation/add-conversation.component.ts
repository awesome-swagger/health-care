import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-add-conversation',
  templateUrl: './add-conversation.component.html',
  styleUrls: ['./add-conversation.component.scss']
})
export class AddConversationComponent implements OnInit {

  public data = null;
  public userChecked = {};
  public patientChecked = false;

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) {
    // Nothing yet
  }

  ngOnInit(): void {
    if (this.data && this.data.careTeam) {
      Object.keys(this.data.careTeam).forEach((id) => {
        if (id !== this.data.userId) {
          this.userChecked[id] = false;
        }
      });
    }
  }

  public get careTeamMembers(): Array<any> {
    if (this.data && this.data.careTeam) {
      const result = [];
      Object.keys(this.data.careTeam).forEach((id) => result.push(this.data.careTeam[id]));

      return result;
    }

    return [];
  }

  public close(): void {
    this.modals.close(null);
  }

  public continue(): void {
    const members = [];
    Object.keys(this.userChecked).forEach(id => {
      if (this.userChecked[id]) {
        members.push(id);
      }
    });

    members.push(this.data.userId);
    if (this.patientChecked) {
      members.push(this.data.patient.user.id);
    }

    this.store.CarePlan
      .detailRoute('POST', this.data.planId, 'message_recipients', { members })
      .subscribe(res => this.modals.close(res));
  }
}
