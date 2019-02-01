import * as faker from 'faker';
import * as moment from 'moment';

export class HistoryMockData {

   public employees = [
    {
      id: 1,
      first_name: 'Lori',
      last_name: 'Ramirez',
      title: 'RN',
      facilities: [1]
    },
    {
      id: 2,
      first_name: 'John',
      last_name: 'Smith',
      title: 'RN',
      facilities: [1]
    },
    {
      id: 3,
      first_name: 'Paul',
      last_name: 'Gordon',
      title: 'RN',
      facilities: [1]
    }
  ];

  public tasks = [
    {
      id: 1,
      name: 'A Task For A Care Provider',
      category: 'notes',
      role: 'Care Provider',
    },
    {
      id: 2,
      name: 'Another Task',
      category: 'interaction',
      role: 'Dietican',
    },
    {
      id: 3,
      name: 'A Task With A Long Name For A Psychiatric Consultant',
      category: 'coordination',
      role: 'Psychiatric Consultant',
    },
  ];

  public results = [];

  constructor() {
    this.tasks.forEach((task) => {
      this.generateRandomResults(task.id);
    });
  }

	public generateRandomId() {
		return Math.floor(Math.random() * 99999) + 1;
	}

	private pad(number, length) {
		let str = '' + number;
		while (str.length < length) {
			str = '0' + str;
		}
		return str;
	}

	private generateRandomTime() {
		let hour = this.pad(Math.floor(Math.random() * 23) + 1, 2);
		let minute = this.pad(Math.floor(Math.random() * 59) + 1, 2);
		return `${hour}:${minute}:00`;
	}

  private generateRandomResults(task) {
    let employee = this.employees[Math.floor(Math.random() * this.employees.length)].id;
    let employeesExcluded = this.employees.filter((obj) => obj.id !== employee);
    let withEmp = employeesExcluded[Math.floor(Math.random() * employeesExcluded.length)].id;
    for (let i = 0; i < 20; i++) {
      let tmpDate = moment().add(-1 * (i), 'days');
      this.results.push({
        id: this.generateRandomId(),
        date: tmpDate,
        createdBy: employee,
        lastEdited: tmpDate.add(-1 * (Math.floor(Math.random() * 10))),
        lastEditedBy: withEmp,
        task: task,
        totalMinutes: Math.floor(Math.random() * 60),
        with: withEmp,
        syncToEHR: Math.random() > .5,
        notes: 'Test note ' + i,
        patientEngagement: Math.floor(Math.random() * 5) + 1
      });
    }
  }
}
