export default {
  patients: [
    {
      id: 1,
      first_name: 'Adam',
      last_name: 'Sanderson',
      facility: 1,
    },
    {
      id: 2,
      first_name: 'Amy',
      last_name: 'Mulhestein',
      facility: 1,
    },
    {
      id: 3,
      first_name: 'Barry',
      last_name: 'Stevenson',
      facility: 1,
    },
    {
      id: 4,
      first_name: 'Larry',
      last_name: 'Norton',
      facility: 2,
    },
  ],
  facilities: [
    {
      id: 1,
      name: 'Canyon View',
      organization: {
        id: 1,
        name: 'Ogden Clinic'
      },
    },
    {
      id: 2,
      name: 'South Ogden Family Medicine',
      organization: {
        id: 1,
        name: 'Ogden Clinic'
      },
    },
  ],
  serviceAreas: [
    {
      id: 1,
      name: 'Bariatrics'
    },
    {
      id: 2,
      name: 'Behavioral Health'
    },
    {
      id: 3,
      name: 'Cardiology'
    },
    {
      id: 4,
      name: 'Internal Medicine'
    },
    {
      id: 5,
      name: 'Oncology'
    },
    {
      id: 6,
      name: 'Orthopedics'
    },
  ],
  billingTypes: [
    {
      id: 1,
      name: 'Remote Patient Management',
      acronym: 'RPM',
      code: 11111,
    },
    {
      id: 2,
      name: 'Behavioral Health Initiative',
      acronym: 'BHI',
      code: 22222,
    },
    {
      id: 3,
      name: 'Psychiatric Collaberative Care Management',
      acronym: 'CoCM',
      code: 333333,
    },
    {
      id: 4,
      name: 'Chronic Care Management',
      acronym: 'CCM',
      code: 44444,
    },
    {
      id: 5,
      name: 'Complex Chronic Care Management',
      acronym: 'CCCM',
      code: 55555,
    },
    {
      id: 6,
      name: 'Transitional Care Management',
      acronym: 'TCM',
      code: 66666,
    },
  ],
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
	billingData: [
    {
      isBilled: false,
      serviceArea: 1,
  		patient: 1,
      careManager: 2,
    	billingPractitioner: 1,
      billingCoordinator: 3,
      entries: [
        {
          name: 'Initial Visit',
          billingType: 3,
          totalMinutes: 60,
          date: 'April 19, 2018',
          description: 'description',
          subtotal: 115.36,
        },
        {
          name: 'Second Visit',
          billingType: 3,
          totalMinutes: 70,
          date: 'April 19, 2018',
          description: 'description',
          subtotal: 145.87,
        },
      ],
      details: [
        {
          action: 'Call with Patient',
          with: 'Lori Rameriz, RN',
          date: 'April 1, 2018',
          time: '9:05 AM',
          duration: 10
        }
      ]
  	},
    ///////////////////////////////////////////////////////////////////////////
    {
      isBilled: true,
      serviceArea: 2,
  		patient: 2,
      careManager: 1,
    	billingPractitioner: 2,
      billingCoordinator: 3,
      entries: [
        {
          name: 'Initial Visit',
          billingType: 2,
          totalMinutes: 20,
          date: 'April 19, 2018',
          description: 'description',
          subtotal: 115.01,
        },
      ],
      details: [
        {
          action: 'Call with Patient',
          with: 'Lori Rameriz, RN',
          date: 'April 1, 2018',
          time: '9:05 AM',
          duration: 10
        }
      ]
  	},
    ///////////////////////////////////////////////////////////////////////////
    {
      isBilled: false,
      serviceArea: 3,
  		patient: 4,
      careManager: 1,
    	billingPractitioner: 3,
      billingCoordinator: 2,
      entries: [
        {
          name: 'Initial Visit',
          billingType: 2,
          totalMinutes: 20,
          date: 'April 19, 2018',
          description: 'description',
          subtotal: 115.01,
        },
      ],
      details: [
        {
          action: 'Call with Patient',
          with: 'Lori Rameriz, RN',
          date: 'April 1, 2018',
          time: '9:05 AM',
          duration: 10
        }
      ]
  	},
    ///////////////////////////////////////////////////////////////////////////
  ],
}
