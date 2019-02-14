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

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) { }

  ngOnInit() {
    if (this.data && this.data.careTeam) {
      Object.keys(this.data.careTeam).forEach((id) => {
        if (id !== this.data.userId) {
          this.userChecked[id] = false;
        }
      })
    }
  }

  public get careTeamMembers() {
    if (this.data && this.data.careTeam) {
      const result = [];
      Object.keys(this.data.careTeam).forEach((id) => {
        result.push(this.data.careTeam[id])
      })
      return result;
    }
    return [];
  }

  public close() {
    this.modals.close(null);
  }

  public continue() {
    const members = [];
    Object.keys(this.userChecked).forEach(id => {
      if (this.userChecked[id]) {
        members.push(id);
      }
    })
    members.push(this.data.userId);
    this.store.CarePlan.detailRoute('POST', this.data.planId, 'message_recipients', {
      members
    }).subscribe(res => {
      this.modals.close(res);
    })
  }

}
