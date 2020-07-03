export default {
  carePlans: [
    {
      name: 'Depression',
      type: 'CoCM',
      careTeam: [
        'Susan Smith, RN',
        'Jason Hannigan, PA',
        'Melanie Benson, CRNA',
      ],
      week: 5,
      totalWeeks: 16,
      daysSinceContact: 3,
      problems: 1,
      time: '1:50',
      riskLevel: 32,
    },
    {
      name: 'Anxiety',
      type: 'CoCM',
      careTeam: [
        'Lori Ramirez, RN',
        'Jason Hannigan, PA',
      ],
      week: 7,
      totalWeeks: 12,
      daysSinceContact: 4,
      problems: 4,
      time: ':57',
      riskLevel: 84,
    }
  ],
  patient: {
    user: {
      first_name: 'Theresa',
      last_name: 'Beckstrom',
    },
    statistics: {
      readmits: 2,
      readmitPercent: 33.3,
      readmitCost: '$10,975',
      edVisits: 3,
      opioidUse: 5,
      admits: 4,
      avgStay: 2.5,
      pcpVisits: 7,
      specialistVisits: 2,
      totalCost: '$45,890',
    },
    medications: [
      'Zoloft',
      'Glumetza',
      'Lexapro',
    ],
    diagnoses: [
      'Depression',
      'Anxiety',
      'Diabetes',
    ],
    procedures: [
      'Double Bypass',
      'Bariatric Surgery',
      'Hip Replacement',
    ],
    profile: {
      age: 76,
      dob: 'May 23, 1959',
      gender: 'Female',
      insurance: 'BCBS',
      secondaryIns: 'Medicare',
      MRN: '345752671',
      height: `5' 2"`,
      ethnicity: 'Hispanic',
      cognitiveAbility: 'high',
    },
    address: {
      street: '519 E 2000 N',
      apt: '',
      city: 'North Ogden',
      state: 'UT',
      zip: '84414',
    },
    emergencyContact: {
      name: 'Sally Beckstrom',
      relationship: 'Daughter',
      phone: '(555)666-7777',
      email: 'sally@example.com',
    },
    communication: {
      email: 'theresabeckstrom@example.com',
      phone: '(555)111-2222',
      commPreference: 'In-App Message',
    }
  }
}