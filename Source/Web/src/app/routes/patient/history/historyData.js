export default {
  employees: [
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
  ],
  tasks: [
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
  ],
  results: [
    {
      date: 'Mar 15, 2018',
      time: '8:02 AM',
      createdBy: 1,
      task: 1,
      totalMinutes: 10,
      with: 2,
      syncToEHR: false,
      notes: 'Notes for this task. Notes for this task. Notes for this task. Notes for this task. Notes for this task. Notes for this task.',
      patientEngagement: 5,
    },
    {
      date: 'Mar 14, 2018',
      time: '10:45 AM',
      createdBy: 2,
      task: 2,
      totalMinutes: 15,
      with: 1,
      syncToEHR: true,
      notes: 'Notes for this task. Notes for this task.',
      patientEngagement: 3,
    },
  ]
}
