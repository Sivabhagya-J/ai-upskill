import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { Home, FolderOpen, CheckSquare, ChevronRight, BarChart3, Users } from 'lucide-react'

const Sidebar = () => {
  const [expandedMenus, setExpandedMenus] = useState<Record<string, boolean>>({})

  const toggleMenu = (menuKey: string) => {
    setExpandedMenus(prev => ({
      ...prev,
      [menuKey]: !prev[menuKey]
    }))
  }

  const navItems = [
    { 
      path: '/dashboard', 
      label: 'Dashboard', 
      icon: Home,
      type: 'link'
    },
    { 
      label: 'Project Management', 
      icon: FolderOpen,
      type: 'menu',
      key: 'projects',
      items: [
        { path: '/projects', label: 'All Projects', icon: FolderOpen },
        { path: '/projects/active', label: 'Active Projects', icon: BarChart3 },
      ]
    },
    { 
      label: 'Task Management', 
      icon: CheckSquare,
      type: 'menu',
      key: 'tasks',
      items: [
        { path: '/tasks', label: 'All Tasks', icon: CheckSquare },
        { path: '/tasks/my-tasks', label: 'My Tasks', icon: Users },

      ]
    },

  ]

  return (
    <aside className="w-64 bg-gradient-to-b from-white to-gray-50 shadow-sm border-r border-gray-200 min-h-screen">
      <nav className="mt-8">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon
            
            if (item.type === 'link' && item.path) {
              return (
                <li key={item.path}>
                  <NavLink
                    to={item.path}
                                      className={({ isActive }) =>
                    `flex items-center space-x-3 px-6 py-3 text-sm font-medium transition-all duration-200 rounded-lg mx-2 ${
                      isActive
                        ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 border border-blue-200 shadow-sm'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900 hover:shadow-sm'
                    }`
                  }
                  >
                    <Icon className="h-5 w-5" />
                    <span>{item.label}</span>
                  </NavLink>
                </li>
              )
            }
            
            if (item.type === 'menu' && item.key) {
              const isExpanded = expandedMenus[item.key]
              return (
                <li key={item.key}>
                  <button
                    onClick={() => toggleMenu(item.key!)}
                    className={`w-full flex items-center justify-between px-6 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-all duration-200 rounded-lg mx-2 ${
                      isExpanded ? 'bg-gray-100 shadow-sm' : ''
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className="h-5 w-5" />
                      <span>{item.label}</span>
                    </div>
                    <ChevronRight className={`h-4 w-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                  </button>
                  
                  {isExpanded && item.items && (
                    <ul className="ml-6 mt-1 space-y-1">
                      {item.items.map((subItem) => {
                        const SubIcon = subItem.icon
                        return (
                          <li key={subItem.path}>
                            <NavLink
                              to={subItem.path}
                                                              className={({ isActive }) =>
                                  `flex items-center space-x-3 px-4 py-2 text-sm font-medium transition-all duration-200 rounded-lg ${
                                    isActive
                                      ? 'bg-blue-50 text-blue-700 border border-blue-200 shadow-sm'
                                      : 'text-gray-500 hover:bg-gray-100 hover:text-gray-700 hover:shadow-sm'
                                  }`
                                }
                            >
                              <SubIcon className="h-4 w-4" />
                              <span>{subItem.label}</span>
                            </NavLink>
                          </li>
                        )
                      })}
                    </ul>
                  )}
                </li>
              )
            }
            
            return null
          })}
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar 