import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div className="flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-6 md:mb-0 md:pr-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Tennis Tournament Analysis System
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
              A multi-agent AI system designed to help tennis players improve their skills by analyzing professional tournaments and providing personalized recommendations.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link 
                href="/match-analysis" 
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
              >
                Analyze Matches
              </Link>
              <Link 
                href="/skill-development" 
                className="bg-white dark:bg-gray-700 text-indigo-600 dark:text-indigo-400 border border-indigo-600 dark:border-indigo-400 font-medium py-2 px-4 rounded-md hover:bg-indigo-50 dark:hover:bg-gray-600 transition-colors"
              >
                Develop Skills
              </Link>
            </div>
          </div>
          <div className="md:w-1/2">
            <Image
              src="/tennis-court.svg"
              alt="Tennis Court"
              width={500}
              height={300}
              className="rounded-lg shadow-lg"
            />
          </div>
        </div>
      </div>

      {/* Recent Analyses Section */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recent Analyses</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {[1, 2, 3].map((item) => (
          <div key={item} className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
            <div className="h-40 bg-gray-200 dark:bg-gray-700 relative">
              <div className="absolute inset-0 flex items-center justify-center text-gray-500 dark:text-gray-400">
                Match Preview Image
              </div>
            </div>
            <div className="p-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Djokovic vs. Nadal - French Open 2024
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
                Analysis of key tactical patterns and technical execution in the French Open final.
              </p>
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-500 dark:text-gray-400">May 2, 2025</span>
                <Link 
                  href="/match-analysis/1" 
                  className="text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300"
                >
                  View Analysis →
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions Section */}
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Quick Actions</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: "Analyze New Match", icon: "🎾", link: "/match-analysis/new" },
          { title: "View Skill Progress", icon: "📈", link: "/skill-development/progress" },
          { title: "Training Recommendations", icon: "🏋️", link: "/skill-development/training" },
          { title: "Tournament Calendar", icon: "📅", link: "/tournaments" }
        ].map((action, index) => (
          <Link 
            key={index}
            href={action.link}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow flex items-center"
          >
            <span className="text-2xl mr-3">{action.icon}</span>
            <span className="text-gray-900 dark:text-white font-medium">{action.title}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
