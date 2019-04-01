import { Component, OnInit } from '@angular/core';
import {
  groupBy as _groupBy,
  uniqBy as _uniqBy,
} from 'lodash';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-add-stream',
  templateUrl: './add-stream.component.html',
  styleUrls: ['./add-stream.component.scss'],
})
export class AddStreamComponent implements OnInit {

  public data = null;
  public totalPatients = 0;
  public careMessages = [];
  public searchInput = '';
  public careMessagesShown = [];
  public selectedTemplate = null;
  public editingTemplate = false;
  public createStream = false;
  public newStreamName = '';

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.editingTemplate = this.data.editingTemplate;
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      this.store.InfoMessageQueue.readListPaged({
        is_available: true,
      }).subscribe(
        (data) => {
          this.careMessages = data;
          this.careMessagesShown = _uniqBy(this.careMessages, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {}
      );
    }
  }

  public filterMessages() {
    let matches = this.careMessages.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.careMessagesShown = _uniqBy(matches, (obj) => obj.name);
  }

  public selectMessage(message) {
    if (message.edit || message.delete) {
      return;
    }
    this.selectedTemplate = message;
  }

  public uniqByNameCount(message) {
    let messages = this.careMessages.filter(
      (obj) => obj.name === message.name
    ).filter(
      (obj) => obj.is_active === true
    );
    return messages.length;
  }

  public clickEditMessage(message, e) {
    e.stopPropagation();
    message.edit = !message.edit;
    message.origName = message.name;
  }

  public clickUndoName(message, e) {
    e.stopPropagation();
    message.edit = !message.edit;
    message.name = message.origName;
  }

  public updateMessageName(message, e) {
    e.stopPropagation();
    let messages = this.careMessages.filter((obj) => obj.name === message.origName || obj.name === message.name);
    messages.forEach((obj) => {
      let updateSub = this.store.InfoMessageQueue.update(obj.id, {
        name: message.name,
      }, true).subscribe(
        (resp) => {
          obj.name = message.name;
          message.edit = false;
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public clickDeleteMessage(message, e) {
    e.stopPropagation();
    message.delete = true;
  }

  public clickUndoDelete(message, e) {
    e.stopPropagation();
    message.delete = false;
  }

  public confirmDeleteMessage(message, e) {
    e.stopPropagation();
    let messages = this.careMessages.filter((obj) => obj.name === message.origName || obj.name === message.name);
    messages.forEach((obj) => {
      let updateSub = this.store.InfoMessageQueue.update(obj.id, {
        is_available: false,
        is_active: false
      }, true).subscribe(
        (resp) => {
          let index = this.careMessages.findIndex((a) => a.id === resp.id);
          this.careMessages.splice(index, 1);
          message.delete = false;
          this.careMessagesShown = _uniqBy(this.careMessages, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public addStream(streamName, e) {
    if (streamName.length <= 0) {
      return;
    }
    let newStream = {
      name: streamName,
      plan_template: this.data.planTemplateId,
      type: 'education',
    }
    let createSub = this.store.InfoMessageQueue.create(newStream).subscribe(
      (resp) => {
        this.careMessages.push(resp);
        this.createStream = false;
        let modalData = {
          nextAction: 'create-stream',
          message: resp,
        };
        this.modal.close(modalData);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public clickCancel() {
    this.modal.close(null);
  }

  public clickNext() {
    let newMessage = {
      name: this.selectedTemplate.name,
      plan_template: this.data.planTemplateId,
      type: 'education',
    };
    let createSub = this.store.InfoMessageQueue.create(newMessage).subscribe(
      (resp) => {
        this.careMessages.push(resp);
        this.createStream = false;
        this.modal.close({
          nextAction: 'create-stream',
          message: resp,
        });
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public nextDisabled() {
    return !this.selectedTemplate;
  }
}
