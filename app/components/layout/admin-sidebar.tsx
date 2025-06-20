
'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Users,
  FolderOpen,
  ShoppingCart,
  Calculator,
  Calendar,
  Package,
  Settings,
  Menu,
  X,
  BarChart3,
  User,
  LogOut,
  ChevronDown
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { signOut, useSession } from 'next-auth/react';

const menuItems = [
  {
    title: 'Дашборд',
    href: '/admin',
    icon: LayoutDashboard,
  },
  {
    title: 'CRM',
    href: '/admin/crm',
    icon: Users,
  },
  {
    title: 'Проекты',
    href: '/admin/projects',
    icon: FolderOpen,
  },
  {
    title: 'Заказы',
    href: '/admin/orders',
    icon: ShoppingCart,
  },
  {
    title: 'Сметы',
    href: '/admin/estimates',
    icon: Calculator,
  },
  {
    title: 'Календарь',
    href: '/admin/calendar',
    icon: Calendar,
  },
  {
    title: 'Материалы',
    href: '/admin/materials',
    icon: Package,
  },
  {
    title: 'Отчеты',
    href: '/admin/reports',
    icon: BarChart3,
  },
  {
    title: 'Настройки',
    href: '/admin/settings',
    icon: Settings,
  },
];

interface AdminSidebarProps {
  className?: string;
}

export function AdminSidebar({ className }: AdminSidebarProps) {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const pathname = usePathname();
  const { data: session } = useSession();

  const handleSignOut = () => {
    signOut({ callbackUrl: '/auth/signin' });
  };

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isMobileOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
            onClick={() => setIsMobileOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Mobile menu button */}
      <button
        onClick={() => setIsMobileOpen(!isMobileOpen)}
        className="fixed top-4 left-4 z-50 p-2 bg-slate-800 text-white rounded-lg lg:hidden"
      >
        {isMobileOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{
          x: isMobileOpen ? 0 : '-100%',
        }}
        className={cn(
          'fixed left-0 top-0 z-40 h-full w-72 bg-slate-900 shadow-lg lg:translate-x-0 lg:static lg:z-auto',
          className
        )}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-slate-700">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-teal-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">BM</span>
              </div>
              <div>
                <h1 className="text-white font-semibold text-lg">BaiMuras</h1>
                <p className="text-slate-400 text-xs">Админ панель</p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || 
                (item.href !== '/admin' && pathname.startsWith(item.href));

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsMobileOpen(false)}
                  className={cn(
                    'flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                    isActive
                      ? 'bg-teal-500 text-white shadow-lg'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  )}
                >
                  <Icon size={18} />
                  <span>{item.title}</span>
                </Link>
              );
            })}
          </nav>

          {/* User menu */}
          <div className="p-4 border-t border-slate-700">
            <div className="relative">
              <button
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="flex items-center justify-between w-full p-3 text-slate-300 hover:bg-slate-800 rounded-lg transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-slate-600 rounded-full flex items-center justify-center">
                    <User size={16} />
                  </div>
                  <div className="text-left">
                    <div className="text-sm font-medium text-white">
                      {session?.user?.name || session?.user?.username}
                    </div>
                    <div className="text-xs text-slate-400">
                      {session?.user?.email}
                    </div>
                  </div>
                </div>
                <ChevronDown 
                  size={16} 
                  className={cn(
                    'transition-transform duration-200',
                    userMenuOpen && 'rotate-180'
                  )}
                />
              </button>

              <AnimatePresence>
                {userMenuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute bottom-full left-0 w-full mb-2 bg-slate-800 rounded-lg shadow-lg border border-slate-700"
                  >
                    <button
                      onClick={handleSignOut}
                      className="flex items-center space-x-3 w-full p-3 text-slate-300 hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      <LogOut size={16} />
                      <span className="text-sm">Выйти</span>
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </motion.aside>
    </>
  );
}
