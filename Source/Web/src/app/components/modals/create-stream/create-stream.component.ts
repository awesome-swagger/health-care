import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { omit as _omit } from 'lodash';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-create-stream',
  templateUrl: './create-stream.component.html',
  styleUrls: ['./create-stream.component.scss'],
})
export class CreateStreamComponent implements OnInit {

  public data = null;
  public stream: any = {};
  public streamForm: FormGroup = null;
  public messageTooltipOpen = false;
  public deleteMessageOpen = {};

  constructor(
    private store: StoreService,
    private modal: ModalService,
  ) { }

  public tooltipCMS0Open
  public tooltipCMS1Open
  public deleteM0;
  public deleteM1;
  public deleteM2;
  public showAddMessageForm;

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.stream = this.data.stream ? this.data.stream : {};
      this.initForm(this.stream);
    }
  }

  public initForm(stream) {
    this.streamForm = new FormGroup({
      name: new FormControl(stream.name),
      type: new FormControl(stream.type)
    });
  }

  public clickAddMessage() {
    if (!this.stream.messages) {
      this.stream.messages = [];
    }
    this.stream.messages.push({
      queue: this.stream.id,
      text: '',
    });
  }

  public createMessage(message) {
    let promise = new Promise((resolve, reject) => {
      let createSub = this.store.InfoMessage.create(message).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          createSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public updateMessage(message) {
    let promise = new Promise((resolve, reject) => {
      let updateSub = this.store.InfoMessage.update(message.id, message, true).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          updateSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public deleteMessage(message) {
    let promise = new Promise((resolve, reject) => {
      let deleteSub = this.store.InfoMessage.destroy(message.id).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          deleteSub.unsubscribe();
        }
      )
    });
    return promise;
  }

  public createOrUpdateAllMessages() {
    if (!this.stream.messages) {
      return;
    }
    let promises = [];
    this.stream.messages.forEach((message, i) => {
      message.queue = this.stream.id;
      if (!message.id) {
        promises.push(this.createMessage(message));
      } else {
        promises.push(this.updateMessage(message));
      }
    });
    return Promise.all(promises);
  }

  public updateStream() {
    let keys = ['name', 'type'];
    keys.forEach((key) => {
     if (this.streamForm.value[key] != undefined) {
        this.stream[key] = this.streamForm.value[key];
      }
    });
    let promise = new Promise((resolve, reject) => {
      this.stream.plan_template = this.data.planTemplateId;
      let streamWithoutMessages = _omit(this.stream, 'messages');
      if (this.stream.id) {
        let updateSub = this.store.InfoMessageQueue.update(streamWithoutMessages.id, streamWithoutMessages, true)
          .subscribe(
            (res) => resolve(res),
            (err) => reject(err),
            () => {
              updateSub.unsubscribe();
            }
          );
      } else {
        let createSub = this.store.InfoMessageQueue.create(streamWithoutMessages)
          .subscribe(
            (res) => resolve(res),
            (err) => reject(err),
            () => {
              createSub.unsubscribe();
            }
          );
      }
    });
    return promise;
  }

  public closeDeleteMessages() {
    let keys = Object.keys(this.deleteMessageOpen);
    keys.forEach((key) => {
      this.deleteMessageOpen[key] = false;
    });
  }

  public clickDeleteMessage(message) {
    let messageIndex = this.stream.messages.findIndex((obj) => {
      return obj.id === message.id;
    });
    this.deleteMessage(message).then(() => {
      this.closeDeleteMessages();
      this.stream.messages.splice(messageIndex, 1);
    });
  }

  public clickSave() {
    this.updateStream().then((stream: any) => {
      this.stream.id = stream.id;
      this.createOrUpdateAllMessages().then(() => {
        this.modal.close(this.stream);
      });
    });
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
