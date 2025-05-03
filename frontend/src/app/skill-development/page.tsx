import React from 'react';

export default function SkillDevelopmentPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Skill Development
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
          Personalized tennis skill development recommendations based on professional match analysis.
        </p>
      </div>

      {/* Skill Areas Section */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Skill Areas</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[
          { title: "Technical Skills", icon: "🎯", description: "Stroke techniques, footwork, and movement patterns" },
          { title: "Tactical Skills", icon: "🧠", description: "Game strategy, shot selection, and court positioning" },
          { title: "Mental Skills", icon: "🧘", description: "Focus, resilience, and pressure management" }
        ].map((skill, index) => (
          <div key={index} className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <span className="text-3xl mr-3">{skill.icon}</span>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{skill.title}</h3>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-4">{skill.description}</p>
            <a 
              href={`/skill-development/${skill.title.toLowerCase().replace(' ', '-')}`}
              className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium"
            >
              View recommendations →
            </a>
          </div>
        ))}
      </div>

      {/* Recent Recommendations Section */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recent Recommendations</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden mb-8">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Skill
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Recommendation
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Priority
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Date
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {[
              { skill: "Forehand", recommendation: "Improve topspin generation", priority: "High", status: "In Progress", date: "May 1, 2025" },
              { skill: "Serve", recommendation: "Develop second serve consistency", priority: "High", status: "Not Started", date: "May 1, 2025" },
              { skill: "Backhand", recommendation: "Work on down-the-line accuracy", priority: "Medium", status: "Completed", date: "Apr 28, 2025" },
              { skill: "Volley", recommendation: "Practice low volley technique", priority: "Medium", status: "Not Started", date: "Apr 27, 2025" },
              { skill: "Mental", recommendation: "Develop pre-point routine", priority: "High", status: "In Progress", date: "Apr 25, 2025" },
            ].map((rec, index) => (
              <tr key={index}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  {rec.skill}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                  {rec.recommendation}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    rec.priority === "High" 
                      ? "bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100" 
                      : rec.priority === "Medium"
                      ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100"
                      : "bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100"
                  }`}>
                    {rec.priority}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    rec.status === "Completed" 
                      ? "bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100" 
                      : rec.status === "In Progress"
                      ? "bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100"
                      : "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300"
                  }`}>
                    {rec.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                  {rec.date}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Progress Tracking Section */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Skill Progress</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Technical Skills</h3>
            <div className="space-y-4">
              {[
                { skill: "Forehand", progress: 75 },
                { skill: "Backhand", progress: 60 },
                { skill: "Serve", progress: 45 },
                { skill: "Volley", progress: 30 },
              ].map((item, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{item.skill}</span>
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{item.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div 
                      className="bg-indigo-600 h-2.5 rounded-full" 
                      style={{ width: `${item.progress}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Tactical Skills</h3>
            <div className="space-y-4">
              {[
                { skill: "Court Positioning", progress: 65 },
                { skill: "Shot Selection", progress: 50 },
                { skill: "Pattern Recognition", progress: 70 },
                { skill: "Game Management", progress: 55 },
              ].map((item, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{item.skill}</span>
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{item.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div 
                      className="bg-indigo-600 h-2.5 rounded-full" 
                      style={{ width: `${item.progress}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
