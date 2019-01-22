import { AfterViewChecked, Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NavbarService, StoreService } from '../../../services';
import messageStreams from './messageStreamData.js';
import {
  map as _map,
  filter as _filter,
  find as _find,
  groupBy as _groupBy
} from 'lodash';
import * as moment from 'moment';

@Component({
  selector: 'app-patient-messaging',
  templateUrl: './messaging.component.html',
  styleUrls: ['./messaging.component.scss'],
})
export class PatientMessagingComponent implements AfterViewChecked, OnDestroy, OnInit {

  public patient = null;

  public messageStreams = [];
  public currentStream = null;

  public newMessageText = '';

  @ViewChild('chatBox') private chatBox: ElementRef;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: StoreService,
    private nav: NavbarService,
  ) { }


  public ngOnInit() {
    this.messageStreams = messageStreams;
    this.currentStream = this.messageStreams[0];
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.store.PatientProfile.read(params.patientId).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        },
        (err) => {},
        () => {},
      );
    });
    this.chatBox.nativeElement.scrollTop = this.chatBox.nativeElement.scrollHeight + 64;
    this.scrollBottom();
  }

  public ngAfterViewChecked() {
    this.scrollBottom();
  }

  public ngOnDestroy() { }

  public scrollBottom() {
    this.chatBox.nativeElement.scrollTop = this.chatBox.nativeElement.scrollHeight + 64;
  }

  public getParticipants(stream) {
    const participants = _filter(stream.participants, p => !p.isCurrentUser);
    if (participants.length === 1) {
      const recipient = participants[0];
      return `${recipient.firstName} ${recipient.lastName}${recipient.title ? ', ' : ''}${recipient.title}`;
    }
    return _map(participants, p => p.lastName).join(', ');
  }

  public getLastMessageTime(stream) {
    const time = moment(stream.messages[stream.messages.length - 1].date);
    if (moment().diff(time, 'days') === 0) {
      return time.format('h:mm')
    } else if (moment().diff(time, 'days') <= 6) {
      return time.format('dddd')
    } else {
      return time.format('MM/DD/YY');
    }
  }

  public changeStream(stream) {
    this.currentStream = _find(this.messageStreams, s => s.id === stream.id);
  }

  public messagesByDay(stream) {
    const grouped = _groupBy(stream.messages, m => moment(m.date).format('dddd'));
    const keys = Object.keys(grouped);
    return _map(keys, k => grouped[k]);
  }

  public getDay(message) {
    const date = moment(message.date);
    if (moment().diff(date, 'days') === 0) {
      return 'Today';
    } else if (moment().diff(date, 'days') === 1) {
      return 'Yesterday';
    } else if (moment().diff(date, 'days') <= 6) {
      return date.format('dddd');
    } else {
      return date.format('MM/DD/YY');
    }
  }

  public getTime(message) {
    return moment(message.date).format('h:mm A');
  }

  public getUser(stream, message) {
    return _find(stream.participants, p => p.id === message.userId);
  }

  public getNameAndTitle(user){
    return `${user.firstName} ${user.lastName}${user.title ? ', ' : ''}${user.title ? user.title : ''}`;
  }

  public isSelf(stream, message) {
    return this.getUser(stream, message).isCurrentUser;
  }

  public get currentUser() {
    if (this.currentStream) {
      return _find(this.currentStream.participants, p => p.isCurrentUser);
    }
    return null;
  }

  public addMessage() {
    this.currentStream.messages.push({
      text: this.newMessageText,
      userId: this.currentUser.id,
      date: moment().format()
    })

    this.newMessageText = '';
  }
}
