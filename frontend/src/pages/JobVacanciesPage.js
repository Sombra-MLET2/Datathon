import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Paper, 
  Button, 
  AppBar, 
  Toolbar, 
  IconButton, 
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  Dashboard as DashboardIcon,
  Person as PersonIcon,
  Work as WorkIcon,
  ExitToApp as LogoutIcon,
  Visibility as VisibilityIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const JobVacanciesPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalVacancies, setTotalVacancies] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  useEffect(() => {
    fetchVacancies();
  }, [page, rowsPerPage]);

  const fetchVacancies = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/job-vacancies/?page=${page + 1}&page_size=${rowsPerPage}`);
      setVacancies(response.data.items);
      setTotalVacancies(response.data.total);
      setTotalPages(response.data.total_pages);
      setError('');
    } catch (err) {
      console.error('Error fetching vacancies:', err);
      setError('Failed to load job vacancies. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleViewVacancy = (id) => {
    navigate(`/job-vacancies/${id}`);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const navigateTo = (path) => {
    navigate(path);
  };

  const drawerContent = (
    <Box sx={{ width: 250 }} role="presentation">
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" color="primary">Sombra Recruitment</Typography>
        <Typography variant="body2" color="text.secondary">
          {user?.email}
        </Typography>
      </Box>
      <Divider />
      <List>
        <ListItem button onClick={() => navigateTo('/dashboard')}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button onClick={() => navigateTo('/applicants')}>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <ListItemText primary="Applicants" />
        </ListItem>
        <ListItem button selected onClick={() => navigateTo('/job-vacancies')}>
          <ListItemIcon>
            <WorkIcon color="primary" />
          </ListItemIcon>
          <ListItemText primary="Job Vacancies" />
        </ListItem>
      </List>
      <Divider />
      <List>
        <ListItem button onClick={logout}>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={toggleDrawer}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Job Vacancies
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Button color="inherit" onClick={logout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer}
      >
        {drawerContent}
      </Drawer>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          backgroundColor: (theme) => theme.palette.background.default,
          minHeight: '100vh'
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="h4" gutterBottom>
            Job Vacancies
          </Typography>
          
          <Typography variant="body1" paragraph>
            Browse all available job vacancies in the system.
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}
          
          <Paper sx={{ width: '100%', mb: 2 }}>
            {loading ? (
              <Box display="flex" justifyContent="center" my={5}>
                <CircularProgress />
              </Box>
            ) : (
              <>
                <TableContainer>
                  <Table sx={{ minWidth: 650 }} aria-label="job vacancies table">
                    <TableHead>
                      <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>Title</TableCell>
                        <TableCell>Client</TableCell>
                        <TableCell>Location</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell align="right">Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {vacancies.map((vacancy) => (
                        <TableRow
                          key={vacancy.id}
                          sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                          <TableCell component="th" scope="row">
                            {vacancy.vaga_id}
                          </TableCell>
                          <TableCell>{vacancy.titulo_vaga}</TableCell>
                          <TableCell>{vacancy.cliente}</TableCell>
                          <TableCell>{`${vacancy.cidade}, ${vacancy.estado}, ${vacancy.pais}`}</TableCell>
                          <TableCell>{formatDate(vacancy.data_requicisao)}</TableCell>
                          <TableCell align="right">
                            <Button
                              variant="contained"
                              size="small"
                              startIcon={<VisibilityIcon />}
                              onClick={() => handleViewVacancy(vacancy.id)}
                            >
                              View
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
                <TablePagination
                  rowsPerPageOptions={[10, 25, 50, 100]}
                  component="div"
                  count={totalVacancies}
                  rowsPerPage={rowsPerPage}
                  page={page}
                  onPageChange={handleChangePage}
                  onRowsPerPageChange={handleChangeRowsPerPage}
                />
              </>
            )}
          </Paper>
        </Container>
      </Box>
    </Box>
  );
};

export default JobVacanciesPage;
