import * as faker from 'faker';
import * as moment from 'moment';

export class DetailsMockData {

	public employees = [];
	public facilities = [];
	public goals = [];
	public userTasks = [];
	public careTeamTasks = [];
	public patientTasks = [];
	public assessmentResults = [];
	public symptomResults = [];
	public vitalResults = [];

	constructor() {
		this.facilities = [this.generateRandomFacility()];
		for (let i = 0; i < 10; i++) {
			this.employees.push(this.generateRandomEmployee());
		}
		let goalNames = ['Manage Depression Symptoms', 'Heathier habits and eating.', 'Interact with Family'];
		goalNames.forEach((name) => {
			this.goals.push(this.generateRandomGoal(name));
		});
		let userTaskNames = ['Review Patient Data', 'Schedule Appointment', 'CT Coordination', 'Follow up on labs'];
		userTaskNames.forEach((name) => {
			this.generateUserTasks(name, 12);
		});
		let careTeamTaskNames = ['Patient Call', 'CT Coordination', 'Review Patient Data'];
		careTeamTaskNames.forEach((name) => {
			this.generateCareTeamTasks(name, 12);
		});
		let patientTaskNames = [
			{ name: 'AM Medication', type: 'medication', },
			{ name: '30 min exercise', type: 'task', },
			{ name: 'Blood Pressure', type: 'vital', },
			{ name: 'Resting Heart Rate', type: 'vital', },
			{ name: 'Daily Symptoms Report', type: 'symptoms', },
			{ name: 'General Well-being', type: 'assessment', },
			{ name: 'PM Medication', type: 'medication', },
			{ name: 'Patient Satisfaction', type: 'assessment', },
		];
		patientTaskNames.forEach((obj) => {
			this.generatePatientTasks(obj.name, obj.type, 12);
		});
		let assessmentDetails = [
			{
				name: 'Depression Review', questions: [
					'Rate your happiness level.', 'Rate your pain level.',
					'Rate your energy level.', 'Rate your overall sense of well-being',
				],
			},
			{
				name: 'Another Assessment', questions: [
					'Rate your assessment skills', 'Rate your assessment skills again',
				],
			},
		];
		assessmentDetails.forEach((obj) => {
			this.generateAssessmentResults(obj.name, obj.questions, 30);
		});
		let symptomNames = ['Fatigue', 'Headache', 'Insomnia'];
		symptomNames.forEach((name) => {
			this.generateSymptomResults(name, 12);
		});
		let vitalDetails = [
			{
				name: 'Blood Pressure', questions: [
					'Diastolic', 'Systolic',
				],
			},
			{
				name: 'Sleep', questions: [
					'How many hours of sleep',
				],
			},
		];
		vitalDetails.forEach((obj) => {
			this.generateVitalResults(obj.name, obj.questions, 30);
		});
	}

	private generateRandomId() {
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

	private generateRandomStatus() {
		let statusChoices = ['done', 'done', 'done', 'late', 'late', 'open', 'missed'];
		return statusChoices[Math.floor(Math.random() * statusChoices.length)];
	}

	public generateRandomEmployee() {
		return {
			id: this.generateRandomId(),
			first_name: faker.name.firstName(),
			last_name: faker.name.lastName(),
			title: 'RN',
			facilities: [1],
		};
	}

	public generateRandomFacility() {
		return {
			id: this.generateRandomId(),
			name: 'Canyon View',
			organization: {
				id: this.generateRandomId(),
				name: 'Ogden Clinic'
			},
		};
	}

	public generateRandomGoal(name) {
		return {
			id: this.generateRandomId(),
			name: name,
			progress: Math.floor(Math.random() * 5) + 1,
			lastUpdated: faker.date.past(),
			comments: [
				{
					id: this.generateRandomId(),
					text: 'test',
				}
			],
		};
	}

	public generateUserTasks(name, occurances) {
		let tmpDate = moment().add(-1 * (occurances - 5), 'days');
		for (let i = 0; i < occurances; i++) {
			this.userTasks.push({
				id: this.generateRandomId(),
				name: name,
				date: tmpDate.format('YYYY-MM-DD'),
				appear: this.generateRandomTime(),
				due: this.generateRandomTime(),
				status: this.generateRandomStatus(),
				currentOccurance: i + 1,
				totalOccurances: occurances,
			});
			tmpDate = tmpDate.add(1, 'days');
		}
	}

	public generateCareTeamTasks(name, occurances) {
		let tmpDate = moment().add(-1 * (occurances - 5), 'days');
		for (let i = 0; i < occurances; i++) {
			this.careTeamTasks.push({
				id: this.generateRandomId(),
				name: name,
				date: tmpDate.format('YYYY-MM-DD'),
				appear: this.generateRandomTime(),
				due: this.generateRandomTime(),
				status: this.generateRandomStatus(),
				currentOccurance: i + 1,
				totalOccurances: occurances,
			});
			tmpDate = tmpDate.add(1, 'days');
		}
	}

	public generatePatientTasks(name, type, occurances) {
		let tmpDate = moment().add(-1 * (occurances - 5), 'days');
		for (let i = 0; i < occurances; i++) {
			this.patientTasks.push({
				id: this.generateRandomId(),
				type: type,
				name: name,
				date: tmpDate.format('YYYY-MM-DD'),
				appear: this.generateRandomTime(),
				due: this.generateRandomTime(),
				status: this.generateRandomStatus(),
				currentOccurance: i + 1,
				totalOccurances: occurances,
				averageEngagement: Math.random(),
			});
			tmpDate = tmpDate.add(1, 'days');
		}
	}

	public generateAssessmentResults(name, questionTextArray, occurances) {
		let tmpDate = moment().add(-1 * (occurances - 5), 'days');
		for (let i = 0; i < occurances; i++) {
			this.assessmentResults.push({
				id: this.generateRandomId(),
				name: name,
				date: tmpDate.format('YYYY-MM-DD'),
				tracksOutcome: Math.random() > .5,
				tracksSatisfaction: Math.random() > .5,
				questions: questionTextArray.map((q) => {
					return {
						id: this.generateRandomId(),
						text: q,
						outcome: Math.floor(Math.random() * 5) + 1,
						currentOccurance: i + 1,
						totalOccurances: occurances,
						vsPrev: 'better',
						vsNext: 'none',
						vsPlan: 'average',
					}
				}),
			});
			tmpDate = tmpDate.add(1, 'days');
		}
	}

  public generateSymptomResults(name, occurances) {
		let tmpDate = moment().add(-1 * (occurances - 5), 'days');
		for (let i = 0; i < occurances; i++) {
			this.symptomResults.push({
  			id: this.generateRandomId(),
  			name: name,
				date: tmpDate.format('YYYY-MM-DD'),
  			rating: Math.floor(Math.random() * 5) + 1,
        currentOccurance: i + 1,
        totalOccurances: occurances,
  			vsPrev: 'same',
  			vsNext: 'none',
  			vsPlan: 'average',
  			comment: 'Test'
  		});
			tmpDate = tmpDate.add(1, 'days');
		}
  }

  public generateVitalResults(name, questionTextArray, occurances) {
		let tmpDate = moment().add(-1 * (occurances - 5), 'days');
	  let vitalQuestionTypeChoices = ['boolean', 'time', 'float', 'integer', 'scale', 'string'];
		for (let i = 0; i < occurances; i++) {
			this.vitalResults.push({
  			id: this.generateRandomId(),
  			name: name,
				date: tmpDate.format('YYYY-MM-DD'),
  			questions: questionTextArray.map((q) => {
					return {
  					id: this.generateRandomId(),
  					text: q,
						type: vitalQuestionTypeChoices[Math.floor(Math.random() * vitalQuestionTypeChoices.length)],
      			results: Math.floor(Math.random() * 5) + 1,
            currentOccurance: i + 1,
            totalOccurances: occurances,
  					vsPrev: 'better',
  					vsNext: 'none',
  					vsPlan: 'average',
  					comment: 'Test'
  				}
				}),
  		});
			tmpDate = tmpDate.add(1, 'days');
		}
  }
}
