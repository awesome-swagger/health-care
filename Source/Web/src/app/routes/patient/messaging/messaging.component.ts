import { AfterViewChecked, AfterViewInit, Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService, NavbarService, StoreService, TimeTrackerService } from '../../../services';
import { AddConversationComponent } from './add-conversation/add-conversation.component';
import {
  map as _map,
  filter as _filter,
  find as _find,
  groupBy as _groupBy,
  uniqBy as _uniqBy,
} from 'lodash';
import * as moment from 'moment';
import { ModalService } from '../../../modules/modals';
import { Promise } from 'q';

@Component({
  selector: 'app-patient-messaging',
  templateUrl: './messaging.component.html',
  styleUrls: ['./messaging.component.scss'],
})
export class PatientMessagingComponent implements AfterViewChecked, OnDestroy, OnInit, AfterViewInit {
  public user = null;
  public patient = null;
  public messageStreams = [];
  public messageRecipients = [];
  public careTeam = {};
  public currentStream = null;
  public participants = {};
  public newMessageText: string = '';
  public userId: string = '';
  public planId: string = '';
  public scrolled = false;
  @ViewChild('chatBox')
  private chatBox: ElementRef;
  @ViewChild('imageUpload')
  private imageUpload: ElementRef;

  constructor(
    private auth: AuthService,
    private modals: ModalService,
    private nav: NavbarService,
    private route: ActivatedRoute,
    private router: Router,
    private store: StoreService,
    private timer: TimeTrackerService,
  ) {
    // Nothing yet
  }

  public ngOnInit(): void {
    this.auth.user$.subscribe((user) => {
      if (!user) {
        return;
      }

      this.user = user;
      this.userId = user.user.id;
      this.route.params.subscribe((params) => {
        this.planId = params.planId;
        this.nav.patientDetailState(params.patientId, params.planId);
        this.store.PatientProfile.read(params.patientId).subscribe((patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        });

        this.getCarePlan(params.planId).then((plan: any) => this.timer.startTimer(this.user, plan));

        this.store.CarePlan.detailRoute('GET', params.planId, 'care_team_members').subscribe((res: any) => {
          res.forEach(m => this.careTeam[m.employee_profile.user.id] = m.employee_profile);

          this.store.CarePlan.detailRoute('GET', params.planId, 'message_recipients').subscribe((res: any) => {
            this.messageRecipients = res.results;

            this.messageRecipients.forEach((m, i) => this.getMessageStreams(m, i, params.planId));
            this.initRefreshInterval();
          });
        });
      });
    });

    this.scrollBottom();
  }

  public ngOnDestroy(): void {
    this.timer.stopTimer();
  }

  public getCarePlan(planId: string): Promise<any> {
    const promise = Promise<any>((resolve, reject) => {
      const carePlanSub = this.store.CarePlan.read(planId).subscribe(
        (carePlan) => resolve(carePlan),
        (err) => reject(err),
        () => carePlanSub.unsubscribe(),
      );
    });

    return promise;
  }

  public getMessageStreams(message: { id: string, members: Array<{ id: string }> }, i, planId: string): void {
    const uri = `message_recipients/${message.id}/team_messages`;
    this.store.CarePlan.detailRoute('GET', planId, uri).subscribe((res: any) => {
      this.messageStreams[i] = { id: message.id, participants: [], messages: [] };
      this.messageStreams[i].participants = _map(message.members, id => {
        if (this.careTeam[id]) {
          return {
            id,
            firstName: this.careTeam[id] ? this.careTeam[id].user.first_name : '',
            lastName: this.careTeam[id] ? this.careTeam[id].user.last_name : '',
            title: this.careTeam[id] ? this.careTeam[id].title.abbreviation : '',
            isCurrentUser: id === this.userId,
          }
        }

        if (id === this.patient.user.id) {
          return {
            id,
            firstName: this.patient.user.first_name,
            lastName: this.patient.user.last_name,
            title: 'Patient',
            isCurrentUser: false,
          }
        }
      });

      this.messageStreams[i].messages = _map(res.results, message => {
        return {
          text: message.content,
          image: message.image,
          userId: message.sender.id,
          date: message.created,
        }
      });

      if (i === 0) {
        this.currentStream = this.messageStreams[i];
      }

      setTimeout(() => {
        this.scrollBottom();
      }, 1000);
    });
  }

  public refreshMessages(message: { id: string }, index: number, planId: string): void {
    const uri = `message_recipients/${message.id}/team_messages`;
    this.store.CarePlan.detailRoute('GET', planId, uri).subscribe((res: any) => {
      this.messageStreams[index].messages = _map(res.results, message => {
        return {
          text: message.content,
          userId: message.sender.id,
          date: message.created,
        }
      });
    });
  }

  public initRefreshInterval(): void {
    // setInterval(() => {
    //   this.messageRecipients.forEach((m,i) => {
    //     this.refreshMessages(m,i, this.planId);
    //   })
    // }, 5000)
  }

  public ngAfterViewInit(): void {
    this.scrollBottom();
  }

  public ngAfterViewChecked(): void {
    //this.scrollBottom('ngAfterViewChecked');
  }

  public scrollBottom(): void {
    this.chatBox.nativeElement.scrollTop = this.chatBox.nativeElement.scrollHeight + 64;
  }

  public getParticipants(stream: { participants?: Array<IUserUser> }): string {
    if (stream && stream.participants) {
      const participants: Array<IUserUser> = _filter(stream.participants, p => p && !p.isCurrentUser);
      if (participants.length === 1) {
        const recipient = participants[0];
        return `${recipient.firstName} ${recipient.lastName}${recipient.title ? ', ' : ''}${recipient.title}`;
      }

      return _map(participants, p => p.lastName).join(', ');
    }

    return null;
  }

  public getLastMessageTime(stream: { messages?: Array<{ date: string | Date | moment.Moment }> }): string {
    if (stream && stream.messages && stream.messages.length > 0) {
      const lastMessage = stream.messages[stream.messages.length - 1];
      return `${this.getDay(lastMessage)} at ${this.getTime(lastMessage)}`
    }

    return null;
  }

  public changeStream(stream: { id: string }): void {
    this.currentStream = _find(this.messageStreams, s => s.id === stream.id);
  }

  public messagesByDay(stream: { messages: Array<{ date: string | Date | moment.Moment }> }): Array<any> {
    const grouped = _groupBy(stream.messages, m => moment(m.date).format('dddd'));
    const keys = Object.keys(grouped);

    return _map(keys, k => grouped[k]);
  }

  public getDay(message: { date: string | Date | moment.Moment }): string {
    const date = moment(message.date);
    if (moment().diff(date, 'days') === 0) {
      return 'Today';
    }

    if (moment().diff(date, 'days') === 1) {
      return 'Yesterday';
    }

    if (moment().diff(date, 'days') <= 6) {
      return date.format('dddd');
    }

    return date.format('MM/DD/YY');
  }

  public getTime(message: { date: string | Date | moment.Moment }): string {
    return moment(message.date).format('h:mm A');
  }

  public getUser(stream: { participants: Array<{ id: string }> }, message: { userId: string }): IUserUser {
    if (message.userId === this.userId) {
      return this.user.user;
    }

    return _find(stream.participants, p => p && p.id === message.userId);
  }

  public getNameAndTitle(user: IUserUser): string {
    if (!user) {
      return '';
    }

    return `${this.getName(user)}${user.title ? `, ${user.title}` : ''}`;
  }

  private getName(user: IUserUser): string {
    if (!user) {
      return '';
    }

    // Handle either of the name properties, camelCase or snake_case
    if (user.hasOwnProperty('first_name')) {
      return `${user.first_name} ${user.last_name}`;
    }

    return `${user.firstName} ${user.lastName}`;
  }

  public isSelf(stream: { participants: Array<{ id: string }> }, message: { userId: string }): boolean {
    return !!(this.getUser(stream, message) || {}).isCurrentUser;
  }

  public get currentUser(): IUser {
    if (this.currentStream) {
      return _find(this.currentStream.participants, p => p && p.isCurrentUser);
    }

    return null;
  }

  public addMessage(): void {
    const str = this.newMessageText;
    if (!str || /^\s*$/.test(str)) {
      this.newMessageText = '';
      return;
    }

    const data = { content: this.newMessageText };
    this.uploadMessage(data).then(success => {
      if (success) {
        this.newMessageText = '';
      }
    });
  }

  public openAddConversation(): void {
    const modalData = {
      AddConversationComponent,
      width: '440px',
      data: {
        planId: this.planId,
        userId: this.userId,
        careTeam: this.careTeam,
        patient: this.patient,
      }
    };

    this.modals.open(AddConversationComponent, modalData).subscribe(res => {
      const participants = _map(res.members, id => {
        let messageUser: IUser = id === this.userId
          ? this.user
          : this.patient && this.patient.user && this.patient.user.id === id
            ? this.patient
            : this.careTeam[id];
        messageUser = messageUser || {};
        const user: IUserUser = messageUser.user || { first_name: '', last_name: '' };
        const title: ITitle = messageUser.title || { abbreviation: '' };

        return {
          id,
          firstName: user.first_name,
          lastName: user.last_name,
          title: title.abbreviation,
          isCurrentUser: id === this.userId,
        };
      });

      this.messageStreams.push({ id: res.id, messages: [], participants });
      this.currentStream = this.messageStreams[this.messageStreams.length - 1];
    });
  }

  public processUpload(): void {
    if (this.currentStream === null) {
      return;
    }

    const file: File = this.imageUpload.nativeElement.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.addEventListener('load', () => this.uploadMessage({
      content: file.name,
      image: reader.result
    }));
  }

  private uploadMessage(data: IMessagePostData): Promise<boolean> {
    if (this.currentStream === null) {
      return Promise<boolean>(resolve => resolve(false));
    }

    const uri = `message_recipients/${this.currentStream.id}/team_messages`;
    const promise = Promise<boolean>((resolve, reject) => {
      this.store.CarePlan.detailRoute('POST', this.planId, uri, data).subscribe(
        (res: any) => {
          if (res === null) {
            console.error('Failed to receive message data back from API');
            resolve(false);
            return;
          }

          const msg: IMessageResponse = {
            date: res.created,
            image: res.image,
            text: res.content,
            userId: res.sender.id
          };

          this.currentStream.messages.push(msg);
          this.scrollBottom();

          resolve(true);
        },
        (err) => {
          console.error('Failed to process message upload', err);
          reject(false);
        },
        () => resolve(false)
      );
    });

    return promise;;
  }
}

interface IUserUser {
  first_name?: string,
  firstName?: string,
  isCurrentUser?: boolean,
  last_name?: string,
  lastName?: string,
  title?: string,
}

interface IMessagePostData {
  content: string,
  image?: string | ArrayBuffer
}

interface IMessageResponse {
  date?: string | moment.Moment | Date,
  image?: string,
  text?: string,
  userId?: string,
}

interface ITitle {
  abbreviation?: string
}

interface IUser {
  title?: ITitle,
  user?: IUserUser
}
